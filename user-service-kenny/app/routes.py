import os
import sys
import datetime
import traceback
from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, escape, json, jsonify, Response,
                   Blueprint)
import requests
from . import models

bp = Blueprint('routes', __name__, url_prefix='/')

# # Get user list (based on criteria?)
# @bp.route('/api/user_list', methods=['GET'])
# def user_list():

#     user_list = user_client.get_user_list()

#     print(json.dumps(user_list))

#     return json.dumps(user_list)


###########
# ACCOUNT #
###########
# Create a user
@bp.route('/api/create_account', methods=['GET', 'POST'])
def create_user():
    """
    Create a new user and store in the database.
    """
    content = request.form

    username = content["username"]
    email = content["email"]
    address_1 = content["address_1"]
    address_2 = content["address_2"]
    address_city = content["address_city"]
    address_state = content["address_state"]
    address_zip = content["address_zip"]
    status = 'active'
    # role = content["role"]

    new_user = models.User(username, email, address_1, address_2, address_city,
                           address_state, address_zip, status)#, role)

    models.db.session.add(new_user)
    models.db.session.commit()

    print('okoay')

    return json.dumps({'result': True, 'content': new_user.return_profile()})


# View a user's profile
@bp.route('/api/view_profile/<u_id>', methods=['GET'])
def view_user(u_id):
    """
    View a user's profile. Additional functionality if you are viewing as an
    admin, or if you are viewing your own profile.
    """
    user = models.User.query.get(u_id)
    return jsonify(user.return_profile())


# Update one or more pieces of info about a user
@bp.route('/api/update_profile/<u_id>', methods=['GET'])
def update_user(u_id):
    """
    Update information in a user profile. Can only be done with your own
    profile. (Q: add admin privilege to do this for another user?)
    """
    user = models.User.query.get(u_id)

    content = request.form

    if 'username' in content.keys():
        user.username = content['username']
    if 'email' in content.keys():
        user.email = content['email']
    if 'address_1' in content.keys():
        user.address_1 = content['address_1']
    if 'address_2' in content.keys():
        user.address_2 = content['address_2']
    if 'address_city' in content.keys():
        user.address_city = content['address_city']
    if 'address_state' in content.keys():
        user.address_state = content['address_state']
    if 'address_zip' in content.keys():
        user.address_zip = content['address_zip']

    models.db.session.commit()

    return jsonify(user.return_profile())


# Suspend a user
@bp.route('/api/suspend_user/<u_id>', methods=['GET'])
def suspend_user(u_id):
    """
    Allow a user to self-suspend their account, or an admin to suspend an
    account for a minor violation of site rules.
    """
    user = models.User.query.get(u_id)

    user.status = 'suspended'

    models.db.session.commit()

    return True


# Delete a user
@bp.route('/api/delete_user/<u_id>', methods=['GET'])
def delete_user(u_id):
    """
    Allow a user to self-delete their account, or an admin to delete an
    account for a major violation of site rules.
    """
    user = models.User.query.get(u_id)

    user.status = 'deleted' # do we want this to drop the row instead?

    models.db.session.commit()

    return True


###########
# RATINGS #
###########
# Rate a user
@bp.route('/api/rate_user/<u_id_give>&<u_id_recv>', methods=['GET'])
def rate_user(u_id_give, u_id_recv):
    """
    Allows one user to provide a rating to another user.
    """
    content = request.form

    rater_id = u_id_give
    recipient_id = u_id_recv
    rating = content["rating"]
    review = content["review"]
    timestamp = content["timestamp"]

    new_rating = models.Rating(rater_id, recipient_id, rating, review,
                               timestamp)

    models.db.session.add(new_rating)
    models.db.session.commit()

    return jsonify(new_rating.return_rating())


########
# CART #
########
# Add to cart
@bp.route('/api/add_to_cart/<u_id>&<auc_id>', methods=['GET'])
def add_to_cart(u_id, auc_id):
    """
    Allow a user to add either a victorious auction or a "buy-now" item to
    their cart.
    """

    added_item = models.CartItem(u_id, auc_id)

    models.db.session.add(added_item)
    models.db.session.commit()

    return jsonify(added_item.return_cart_item())


# Remove from cart
@bp.route('/api/remove_from_cart/<u_id>&<auc_id>', methods=['GET'])
def remove_from_cart(u_id, auc_id):
    """
    Allow a user to remove a "buy-now" item from their cart.
    """
    item_to_remove = models.CartItem.query.get(models.CartItem(u_id, auc_id))

    models.db.session.delete(item_to_remove)
    models.db.session.commit()
    return jsonify(item_to_remove.return_cart_item())


# Clear a cart
@bp.route('/api/clear_cart/<u_id>', methods=['GET'])
def clear_cart(u_id):
    """
    Completely clear a user's cart. Should only be called when a payment has
    been processed, because users who win an auction are obligated to pay for
    the won item.
    """
    cart = json.loads(view_cart(u_id))

    for item in cart:
        remove_from_cart(u_id, json.loads(item)['auc_id'])

    return True


# View cart
@bp.route('/api/view_cart/<u_id>', methods=['GET'])
def view_cart(u_id):
    """
    Allow a user to view their own cart.

    Inputs:
     - u_id (string): the username of the user whose cart you need
    Returns:
     - cart (JSON): a jsonified list of CartItem jsons; each CartItem JSON has
       two keys:
         - "username"
         - "auc_id"
    """
    cart = []
    for row in models.CartItem.query.filter_by(username=u_id):
        cart.append(row.to_json())

    return jsonify(cart)


#############
# WATCHLIST #
#############
# Add to watchlist
@bp.route('/api/add_to_watchlist/<u_id>&<auc_id>', methods=['GET'])
def add_to_watchlist(u_id, auc_id):
    """
    Allow a user to add either a current auction or a "buy-now" item to their
    watchlist.
    """

    added_item = models.WatchlistItem(u_id, auc_id)

    models.db.session.add(added_item)
    models.db.session.commit()

    return jsonify(added_item.return_watchlist_item())


# Remove from watchlist
@bp.route('/api/remove_from_watchlist/<u_id>&<auc_id>', methods=['GET'])
def remove_from_watchlist(u_id, auc_id):
    """
    Allow a user to remove an auction or "buy-now" item from their watchlist.
    """
    item_to_remove = models.WatchlistItem.query.get(models.WatchlistItem(u_id,
                                                                         auc_id))

    models.db.session.delete(item_to_remove)
    models.db.session.commit()

    return jsonify(item_to_remove.return_watchlist_item())


# View watchlist
@bp.route('/api/view_watchlist/<u_id>', methods=['GET'])
def view_watchlist(u_id):
    """
    Allow a user to view their own watchlist.
    """
    watchlist = []
    for row in models.WatchlistItem.query.filter_by(username=u_id):
        watchlist.append(row.to_json())

    return jsonify(watchlist)
