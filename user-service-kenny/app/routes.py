
import os
import sys
import datetime
import traceback
from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, escape, json, jsonify, Response,
                   Blueprint)
import requests
from . import user as user

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
@bp.route('/api/create_account', methods=['GET'])
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
    status = content["status"]
    # role = content["role"]

    new_user = user.User(username, email, address_1, address_2, address_city,
                         address_state, address_zip, status)#, role)

    models.db.session.add(new_user)
    models.db.session.commit()

    return new_user.to_json()


# View a user's profile
@bp.route('/api/view_profile/<u_id:int>', methods=['GET'])
def view_user(u_id):
    """
    View a user's profile. Additional functionality if you are viewing as an
    admin, or if you are viewing your own profile.
    """
    pass


# Update one or more pieces of info about a user
@bp.route('/api/update_profile/<u_id:int>', methods=['GET'])
def update_user(u_id):
    """
    Update information in a user profile. Can only be done with your own
    profile. (Q: add admin privilege to do this for another user?)
    """
    pass


# Suspend a user
@bp.route('/api/suspend_user/<u_id:int>', methods=['GET'])
def suspend_user(u_id):
    """
    Allow a user to self-suspend their account, or an admin to suspend an
    account for a minor violation of site rules.
    """
    pass


# Delete a user
@bp.route('/api/delete_user/<u_id:int>', methods=['GET'])
def delete_user(u_id):
    """
    Allow a user to self-delete their account, or an admin to delete an
    account for a major violation of site rules.
    """
    pass

###########
# RATINGS #
###########
# Rate a user
@bp.route('/api/rate_user/<u_id_give:int>&<u_id_recv:int>', methods=['GET'])
def rate_user(u_id_give, u_id_recv):
    """
    Allows one user to provide a rating to another user.
    """
    pass


########
# CART #
########
# Add to cart
@bp.route('/api/add_to_cart/<u_id:int>&<auc_id:int>', methods=['GET'])
def add_to_cart(u_id, auc_id):
    """
    Allow a user to add either a victorious auction or a "buy-now" item to
    their cart.
    """

    added_item = user.CartItem(u_id, auc_id)

    models.db.session.add(added_item)
    models.db.session.commit()

    return added_item.to_json()


# Remove from cart
@bp.route('/api/remove_from_cart/<u_id:int>&<auc_id:int>', methods=['GET'])
def remove_from_cart(u_id, auc_id):
    """
    Allow a user to remove a "buy-now" item to their cart.
    """
    item_to_remove = user.CartItem.query.get(user.CartItem(u_id, auc_id))

	models.db.session.delete(item_to_remove)
	models.db.session.commit()
	return item_to_remove.to_json()


# Clear a cart
@bp.route('/api/clear_cart/<u_id:int>', methods=['GET'])
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
@bp.route('/api/view_cart/<u_id:int>', methods=['GET'])
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
	for row in user.CartItem.query.filter_by(username=u_id):
		cart.append(row.to_json())

	return jsonify(cart)


#############
# WATCHLIST #
#############
# Add to watchlist
@bp.route('/api/add_to_watchlist/<u_id:int>&<auc_id:int>', methods=['GET'])
def add_to_cart(u_id, auc_id):
    """
    Allow a user to add either a victorious auction or a "buy-now" item to
    their cart.
    """
    pass


# Remove from watchlist
@bp.route('/api/remove_from_watchlist/<u_id:int>&<auc_id:int>', methods=['GET'])
def remove_from_cart(u_id, auc_id):
    """
    Allow a user to remove a "buy-now" item to their cart.
    """
    pass


# View watchlist
@bp.route('/api/view_watchlist/<u_id:int>', methods=['GET'])
def view_cart(u_id):
    """
    Allow a user to view their own cart.
    """
    pass
