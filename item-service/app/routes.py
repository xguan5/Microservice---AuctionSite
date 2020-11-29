
import os
import sys
from datetime import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import models as models

bp = Blueprint('routes', __name__, url_prefix='/')

#get all items
@bp.route('/api/items', methods=['GET'])
def get_items():
	all_items = []
	for row in models.Item.query.all():
		all_items.append(row.to_json())
	res = jsonify(all_items)
	return res

#get one item
@bp.route('/api/item/<id>',methods = ['GET'])
def get_item(id):
	item = models.Item.query.get(id)
	return jsonify({'result': item.to_json()})

#create a new item
@bp.route('api/item/create',methods=['POST'])
def create_item():
	#content = request.get_json(force=True)
	content = request.form
	name = content['name']
	description = content['description']
	if 'category' in content.keys():
		category = content['category']
	if 'flag' in content.keys():
		flag = content['flag']

	new_item = models.Item(name,description, category)

	models.db.session.add(new_item)
	models.db.session.commit()

	return jsonify({'result': new_item.to_json()})


#update a item, add item to a category or flag
@bp.route('/api/item/<id>',methods=['PUT'])
def update_item(id):
	item = models.Item.query.get(id)

	content = request.form
	if 'name' in content.keys():
		name = content['name']
		item.name = name
	if 'description' in content.keys():
		description = content['description']
		item.description = description
	if 'category' in content.keys():
		category = content['category']
		item.category_id = category
	if 'flag' in content.keys():
		flag = content['flag']
		item.flag_id = flag

	models.db.session.commit()

	return jsonify({'result': item.to_json()})

#delete item
@bp.route('/api/item/<id>',methods=['DELETE'])
def delete_item(id):
	item = models.Item.query.get(id)
	models.db.session.delete(item)
	models.db.session.commit()
	return jsonify({'result': item.to_json()})

#create a category
@bp.route('api/category/create',methods=['POST'])
def create_category():
	#content = request.get_json(force=True)
	content = request.form
	name = content['name']

	new_category = models.Category(name)

	models.db.session.add(new_category)
	models.db.session.commit()

	return jsonify({'result': new_category.to_json()})

#delete a category
#To do, after delete this category, what happen to the items in this category?
@bp.route('/api/category/<id>',methods=['DELETE'])
def delete_category(id):
	category = models.Category.query.get(id)
	models.db.session.delete(category)
	models.db.session.commit()
	return jsonify({'result': category.to_json()})

#update a category
@bp.route('/api/category/<id>',methods=['PUT'])
def update_category(id):
	category = models.Category.query.get(id)

	content = request.form
	name = content['name']
	category.name = name

	models.db.session.commit()

	return jsonify({'result': category.to_json()})

#get all categories
@bp.route('/api/categories', methods=['GET'])
def get_categories():
	all_categories = []	
	for row in models.Category.query.all():
		all_categories.append(row.to_json())
	res = jsonify(all_categories)
	return res

#get all items for a given category
@bp.route('/api/category/<id>/items', methods=['GET'])
def get_category_items(id):
	category = models.Category.query.get(id)
	all_items = []
	for row in category.items:
		all_items.append(row.to_json())
	res = jsonify(all_items)
	return res

#delete an item from a category just use update item function and update category to null



#create a flag
@bp.route('api/flag/create',methods=['POST'])
def create_flag():
	#content = request.get_json(force=True)
	content = request.form
	name = content['name']

	new_flag = models.Flag(name)

	models.db.session.add(new_flag)
	models.db.session.commit()

	return jsonify({'result': new_flag.to_json()})

#update a flag
@bp.route('/api/flag/<id>',methods=['PUT'])
def update_flag(id):
	flag = models.Flag.query.get(id)

	content = request.form
	if 'name' in content.keys():
		name = content['name']
		item.name = name

	models.db.session.commit()

	return jsonify({'result': flag.to_json()})

#delete a flag
@bp.route('/api/flag/<id>',methods=['DELETE'])
def delete_flag(id):
	flag = models.Flag.query.get(id)
	models.db.session.delete(flag)
	models.db.session.commit()
	return jsonify({'result': flag.to_json()})

#get all flags
@bp.route('/api/flags', methods=['GET'])
def get_flags():
	all_flags = []
	for row in models.Flag.query.all():
		all_flags.append(row.to_json())
	res = jsonify(all_flags)
	return res
#get all items for a given flag
@bp.route('/api/flag/<id>/items', methods=['GET'])
def get_flag_items(id):
	flag = models.Flag.query.get(id)
	all_items = []
	for row in flag.items:
		all_items.append(row.to_json())
	res = jsonify(all_items)
	return res


##delete an item from a flag just use update item function and update flag to null


