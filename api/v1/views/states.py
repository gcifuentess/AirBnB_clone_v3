#!/usr/bin/python3
"""state view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """app_views states"""
    from models import storage
    if request.method == 'GET':
        states_list = list(storage.all("State").values())
        states_json = []
        for state in states_list:
            states_json.append(state.to_dict())
        return jsonify(states_json)
    else:
        content = request.get_json()
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'name' not in content:
            return make_response(jsonify("Missing name"), 400)
        else:
            from models.state import State
            new_state = State(**content)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def states_id(state_id):
    """app_views state_id"""
    from models import storage
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        content = request.get_json()
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'id' in content:
            del content['id']
        if 'created_at' in content:
            del content['created_at']
        if 'updated_at' in content:
            del content['updated_at']
        for key, value in content.items():
            setattr(obj, key, value)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
