import os
import sys
from datetime import datetime, timedelta
import traceback
from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, escape, json, jsonify, Response,
                   Blueprint)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import requests
import email, imaplib
import smtplib, ssl
from . import models

bp = Blueprint('routes', __name__, url_prefix='/')
scheduler = BackgroundScheduler()
scheduler.start()

###########################
# SEND AUTOMATED MESSAGES #
###########################
@bp.route('/api/send_auto_msg', methods=['POST'])
def send_auto_msg():
    """
    Send an automated message that does not need true customization or
    reply.
    """
    content = request.form

    auto_messages = {
        'watchlist match': 'A new item that matches your watchlist has been posted.\nID: {}',
        'new bid': 'A buyer has bid on your item!\nItem name: {}\nAuction ID: {}\nBid amount: {}',
        'outbid': 'Another buyer has outbid you on an auction\nItem name: {}\nAuction ID: {}\nYour bid amount: {}\nTheir bid amount: {}',
        'time': 'An auction you are involved in is ending soon.\nItem name: {}\nAuction ID: {}\nTime remaining:{}'
    }

    auto_subjects = {
        'watchlist match': 'You have a new match from your watchlist!',
        'new bid': 'Someone has bid on your auction!',
        'outbid': 'Someone has outbid you on an auction!',
        'time': 'An auction is ending soon!'
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


@bp.route('/api/schedule_alerts', methods=['POST'])
def schedule_alerts():
    """
    Schedules alerts to start, stop, and remind about each auction.
    """

    content = request.form

    auc_id = content["auc_id"]

    end_time = content["end_time"]
    end_time = datetime.combine(datetime.strptime(end_time, '%Y-%m-%d'),
                                datetime.strptime(end_time, '%H:%M').time())

    start_time = content["start_time"]
    start_time = datetime.combine(datetime.strptime(start_time, '%Y-%m-%d'),
                                  datetime.strptime(start_time, '%H:%M').time())

    # schedule start of auction
    trigger = DateTrigger(run_date=start_time)
    scheduler.add_job(trigger_auction, args=[auc_id, 'start'], trigger=trigger)

    # schedule end of auction
    trigger = DateTrigger(run_date=end_time)
    scheduler.add_job(trigger_auction, args=[auc_id, 'end'], trigger=trigger)

    # schedule 24-hr reminder
    if end_time > datetime.now() + timedelta(hours=24):
        trigger = DateTrigger(run_date=end_time - timedelta(hours=24))
        scheduler.add_job(send_alerts, args=[auc_id, "24 hours"], trigger=trigger)

    # schedule 1-hr reminder
    if end_time > datetime.now() + timedelta(hours=1):
        trigger = DateTrigger(run_date=end_time - timedelta(hours=1))
        scheduler.add_job(send_alerts, args=[auc_id, "1 hour"], trigger=trigger)


def trigger_auction(auc_id, action):
    """
    Start/end an auction.
    """
    url = 'http://auction:5000/api/auction/' + str(auc_id)
    new_status = "Active" if action == "start" else "Completed" # is this the right terminology?
    data = {'status': new_status}

    response = requests.put(url, data=data)


def send_alerts(auc_id, time_remaining):
    """
    Send alerts to seller and all bidders that an auction is ending a certain
    amount of time.
    """
    # first, get the seller
    url = 'http://auction:5000/api/auction/' + str(auc_id)

    auction = requests.get(url)['result']
    seller_id = auction['creator']

    # then, get everyone who has bid (so far)
    url += '/bids'

    buyer_ids = requests.get(url)['result']
    buyer_ids = [buyer[user_id] for buyer in buyer_ids]

    # finally, send an automated email to all of these people
    msg_url = 'http://notification:5000/api/send_auto_msg'
    for user_id in [seller_id] + buyer_ids:
        user_url = 'http://user:5000/api/view_profile/' + user_id
        response = requests.get(msg_url)
        recipient = response["content"]["email"]

        data = {
            'msg': 'time',
            'parameters': [auction["item"], auc_id, time_remaining],
            'user_email': recipient
        }
        requests.post(msg_url, data=data)


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
    return msg.return_email()


@bp.route('/api/get_all_msg', methods=['GET'])
def get_messages():
    """
    Returns all messages that require a reply.
    """
    data = []
    for row in models.Email.query.filter_by(needs_reply=True):
        data.append(row.return_email())

    return jsonify(data)


@bp.route('/api/reply_msg/<msg_id>', methods=['POST'])
def reply_to_message(msg_id):
    """
    Sends a reply to a specific message.
    """

    message = models.Email.query.get(msg_id)
    message.needs_reply = False
    models.db.session.commit()

    content = request.form

    original_email = get_message(msg_id)

    sender = "teambottleneck@gmail.com"
    recipient = original_email["sender"]
    reply_text = content["reply_text"]
    msg = reply_text + "\n\n" + original_email["message"]
    subject = "RE: " + original_email["subject"]

    port = 465  # For SSL
    password = "bottleneck6!"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print('fire away')
        server.login(sender, password)
        server.sendmail(sender, recipient, subject + "\n\n" + msg)

    return 'success'
