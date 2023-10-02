#!/usr/bin/python3
""" State objects API """
from models import storage
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves list of State objects"""
	states = []
	for state in storage.all(State).values():
		states.append(state.to_dict())
	return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
				strict_slashes=False)
def get_state(state_id):
	"""retrieves state object with state_id"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
				strict_slashes=False)
def delete_state(state_id):
	"""deletes state with state_id"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	state.delete()
	storage.save()
	return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
	"""create new state object"""
	if not request.get_json():
		return make_response(jsonify({'error': 'Not a JSON'}), 400)
	if 'name' not in request.get_json():
		return make_response(jsonify({'error': 'Missing name'}), 400)
	state = State(**request.get_json())
	state.save()
	return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
				strict_slashes=False)
def update_state(state_id):
	"""update state object """
	state = storage.get(State, state_id)
	print(state)
	if state is None:
		abort(404)
	if not request.get_json():
		return make_response(jsonify({'error': 'Not a JSON'}), 400)
	for attr, val in request.get_json().items():
		if attr not in ['id', 'created_at', 'updated_at']:
			setattr(state, attr, val)
	state.save()
	return jsonify(state.to_dict())
