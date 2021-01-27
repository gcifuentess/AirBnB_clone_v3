#!/usr/bin/python3
"""API module for HBNB proyect
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == '__main__':
    api_host = getenv("HBNB_API_HOST")
    api_port = getenv("HBNB_API_PORT")
    if api_host is not None and api_port is None:
        app.run(host=api_host, port=api_port, threaded=True)
    elif api_host is None and api_port is not None:
        app.run(host='0.0.0.0', port=api_port, threaded=True)
    elif api_host is not None and api_port is None:
        app.run(host=api_host, port=5000, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
