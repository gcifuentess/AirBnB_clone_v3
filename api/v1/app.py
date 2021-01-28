#!/usr/bin/python3
"""API module for HBNB proyect
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Page Not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    api_host = getenv("HBNB_API_HOST")
    api_port = getenv("HBNB_API_PORT")
    if api_host is not None and api_port is not None:
        app.run(host=api_host, port=api_port, threaded=True)
    elif api_host is None and api_port is not None:
        app.run(host='0.0.0.0', port=api_port, threaded=True)
    elif api_host is not None and api_port is None:
        app.run(host=api_host, port=5000, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
