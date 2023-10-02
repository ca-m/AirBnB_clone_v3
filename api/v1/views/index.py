#!/usr/bin/python3
'''index.py module page'''
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
	"""returns a JSON string of the status in a 200 response"""
	return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
	"""retrieves the number of each objects by type"""
	if request.method == 'GET':
		response = {}
		PLURALS = {
			"Amenity": "amenities",
			"City": "cities",
			"Place": "places",
			"Review": "reviews",
			"State": "states",
			"User": "users"
		}
		for key, value in PLURALS.items():
			response[value] = storage.count(key)
		return jsonify(response)
