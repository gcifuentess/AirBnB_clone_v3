#!/usr/bin/python3
"""users view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/users/', methods=['GET', 'POST'])
@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """app_views users"""
    from models import storage
    if request.method == 'GET':
        users_list = list(storage.all("User").values())
        users_json = []
        for user in users_list:
            users_json.append(user.to_dict())
        return jsonify(users_json)
    else:
        content = request.get_json()
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'email' not in content:
            return make_response(jsonify("Missing email"), 400)
        elif 'password' not in content:
            return make_response(jsonify("Missing password"), 400)
        else:
            from models.user import User
            new_user = User(**content)
            new_user.save()
            return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def users_id(user_id):
    """app_views users_id"""
    from models import storage
    obj = storage.get("User", user_id)
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
        if 'email' in content:
            del content['email']
        for key, value in content.items():
            setattr(obj, key, value)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
