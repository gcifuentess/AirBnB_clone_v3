#!/usr/bin/python3
"""cities view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """app_views cities"""
    from models import storage
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        cities_table = obj.cities
        cities_list = []
        for city in cities_table:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    else:
        content = request.get_json()
        content['state_id'] = state_id
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'name' not in content:
            return make_response(jsonify("Missing name"), 400)
        else:
            from models.city import City
            new_obj = City(**content)
            new_obj.save()
            return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def cities_id(city_id):
    """app_views cities_id"""
    from models import storage
    obj = storage.get("City", city_id)
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
