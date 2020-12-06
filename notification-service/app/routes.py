import os
import sys
import datetime
import traceback
from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, escape, json, jsonify, Response,
                   Blueprint)
import requests
import email, imaplib
import smtplib, ssl
from . import models

bp = Blueprint('routes', __name__, url_prefix='/')

###########################
# SEND AUTOMATED MESSAGES #
###########################
@bp.route('/api/send_auto_msg', methods=['GET'])
def send_auto_msg():
    """
    Send an automated message that does not need true customization or
    reply.
    """
    content = request.form

    auto_messages = {
        'watchlist match': 'A new item that matches your watchlist has been posted.\nID: {}',
        'new bid': 'A buyer has bid on your item!\nItem name: {}\nAuction ID: {}\nBid amount: {}',
        'outbid': 'Another buyer has outbid you on an auction\nItem name: {}\nAuction ID: {}\nYour bid amount: {}\nTheir bid amount: {}'
    }

    auto_subjects = {
        'watchlist match': 'You have a new match from your watchlist!',
        'new bid': 'Someone has bid on your auction!',
        'outbid': 'Someone has outbid you on an auction!'
    }

    msg = auto_messages[content['msg']].format(*content['parameters'])
    subject = auto_subjects[content['msg']]
    sender = "teambottleneck@gmail.com"
    recipient = content['user_email']

    port = 465  # For SSL
    password = "bottleneck6!"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("teambottleneck@gmail.com", password)
        server.sendmail(sender, recipient, subject + '\n\n' + msg)


#############################
# RECEIVE CUSTOMER MESSAGES #
#############################
@bp.route('/api/receive_msg', methods=['GET'])
def receive_messages():
    """
    Connect to our inbox, get all the emails, and store them in our DB
    """
    email_address = 'teambottleneck@gmail.com'
    password = 'bottleneck6!'
    server = 'imap.gmail.com'

    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_address, password)
    mail.select('Inbox')

    status, data = mail.search(None, 'ALL')
    mail_ids = []
    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_from = mail_from[mail_from.find('<')+1:
                                      mail_from.rfind('>')]
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

        new_email = models.Email(int(i), mail_from, "teambottleneck@gmail.com",
                                 mail_subject, mail_content, needs_reply=True)
        try:
            models.db.session.add(new_email)
            models.db.session.commit()
        except Exception as e:
            print('existing')
            pass 
    return 'success'

##############################
# REPLY TO CUSTOMER MESSAGES #
##############################
@bp.route('/api/get_msg/<msg_id>', methods=['GET'])
def get_message(e_id):
    """
    Returns a single message given its message ID.
    """
    msg = models.Email.query.get(e_id)
    return jsonify(msg.return_email())


@bp.route('/api/get_all_msg', methods=['GET'])
def get_messages():
    """
    Returns all messages that require a reply.
    """
    data = []
    for row in models.Email.query.filter_by(needs_reply=True):
        data.append(row.return_email())

    return jsonify(data)


@bp.route('/api/reply_msg/<msg_id>', methods=['GET'])
def reply_to_message(msg_id):
    """
    Sends a reply to a specific message.
    """

    message = models.Email.query.get(msg_id)
    message.needs_reply = False
    models.db.session.commit()
    
    
    content = request.form

    original_email = json.loads(get_message(msg_id))

    sender = "teambottleneck@gmail.com"
    recipient = original_email["sender"]
    reply_text = content["reply_text"]
    msg = reply_text + "\n\n" + original_email["message"]
    subject = "RE: " + original_email["subject"]

    port = 465  # For SSL
    password = "bottleneck6!"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, subject + "\n\n" + msg)
