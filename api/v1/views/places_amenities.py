#!/usr/bin/python3
"""amenities view module"""
from flask import request, make_response, jsonify, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def places_amenities(place_id):
    """app_views places_amenities"""
    from models import storage, storage_t
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    request.method == 'GET'
    amenities_list = []
    if storage_t == "db":
        for amenity in obj.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        for amenity_id in obj.amenity_ids:
            amenity = storage.get("Amenity", amenity_id)
            amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST',
                 'DELETE'], strict_slashes=False)
def places_id_amenities_id(place_id, amenity_id):
    """app_views places_id_amenities_id"""
    from models import storage, storage_t
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'POST':
        if storage_t == "db":
            if amenity in list(place.amenities):
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenities.append(amenity)
                storage.save()
                return make_response(jsonify(amenity.to_dict()), 201)
        else:
            if amenity_id in place.amenity_ids:
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amanity_ids.append(amenity_id)
                storage.save()
                return make_response(jsonify(amenity.to_dict()), 201)
    else:
        if storage_t == "db":
            if amenity not in list(place.amenities):
                abort(404)
            else:
                place.amenities.remove(amenity)
                storage.save()
                return make_response(jsonify({}), 200)
        else:
            if amenity_id not in obj.amenity_ids:
                abort(404)
            else:
                place.amenity_ids.remove(amenity_id)
                storage.save()
                return make_response(jsonify({}), 200)
