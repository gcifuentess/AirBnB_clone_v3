#!/usr/bin/python3
"""index file for views"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """app_views status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """app_views stats"""
    from models import storage
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    for key, value in classes.items():
        classes[key] = storage.count(value)

    return jsonify(classes)
