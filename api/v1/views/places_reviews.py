#!/usr/bin/python3
"""reviews view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews/', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews(place_id):
    """app_views reviews"""
    from models import storage
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        reviews_list = []
        for review in storage.all("Review").values():
            if review.place_id == place_id:
                reviews_list.append(review.to_dict())
        return jsonify(reviews_list)
    else:
        content = request.get_json()
        content["place_id"] = place_id
        if content is None:
            return make_response(jsonify("Not a JSON"), 400)
        elif 'name' not in content:
            return make_response(jsonify("Missing name"), 400)
        elif 'text' not in content:
            return make_response(jsonify("Missing text"), 400)
        elif 'user_id' not in content:
            return make_response(jsonify("Missing user_id"), 400)
        else:
            user_id = content['user_id']
            for user in storage.all("User").values():
                if user.id == user_id:
                    from models.review import Review
                    new_obj = Review(**content)
                    new_obj.save()
                    return make_response(jsonify(new_obj.to_dict()), 201)
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def reviews_id(review_id):
    """app_views reviews_id"""
    from models import storage
    obj = storage.get("Review", review_id)
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
        if 'place_id' in content:
            del content['place_id']
        for key, value in content.items():
            setattr(obj, key, value)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
