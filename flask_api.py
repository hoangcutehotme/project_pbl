from flask import Flask, jsonify

from routes.webserver_route import webserver_route
from routes.detect_api import detect_api
from routes.process_api import process_api

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hoangdev'
app.config['UPLOAD_FOLDER'] = 'static/files'

app.register_blueprint(webserver_route)
app.register_blueprint(detect_api)
app.register_blueprint(process_api)


@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404

