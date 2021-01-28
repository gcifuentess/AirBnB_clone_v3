#!/usr/bin/python3
"""places view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places/', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id):
    """app_views places"""
    from models import storage
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        places_list = []
        for place in storage.all("Place").values():
            if place.city_id == city_id:
                places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        content = request.get_json()
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'name' not in content:
            return make_response(jsonify("Missing name"), 400)
        elif 'user_id' not in content:
            return make_response(jsonify("Missing user_id"), 400)
        else:
            content["city_id"] = city_id
            user_id = content['user_id']
            if storage.get("User", user_id):
                from models.place import Place
                new_obj = Place(**content)
                new_obj.save()
                return make_response(jsonify(new_obj.to_dict()), 201)
            abort(404)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def places_id(place_id):
    """app_views places_id"""
    from models import storage
    obj = storage.get("Place", place_id)
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
        if 'user_id' in content:
            del content['user_id']
        if 'city_id' in content:
            del content['city_id']
        for key, value in content.items():
            setattr(obj, key, value)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
