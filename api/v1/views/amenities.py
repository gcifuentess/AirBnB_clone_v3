#!/usr/bin/python3
"""amanities view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/amenities/', methods=['GET', 'POST'])
@app_views.route('/amenities', methods=['GET', 'POST'])
def amanities():
    """app_views amenities"""
    from models import storage
    if request.method == 'GET':
        amenities_list = list(storage.all("Amenity").values())
        amenities_json = []
        for amenity in amenities_list:
            amenities_json.append(amenity.to_dict())
        return jsonify(amenities_json)
    else:
        content = request.get_json()
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'name' not in content:
            return make_response(jsonify("Missing name"), 400)
        else:
            from models.amenity import Amenity
            new_amenity = Amenity(**content)
            new_amenity.save()
            return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenities_id(amenity_id):
    """app_views amenities_id"""
    from models import storage
    obj = storage.get("Amenity", amenity_id)
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
