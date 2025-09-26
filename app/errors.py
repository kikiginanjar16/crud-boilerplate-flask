
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def http_error(e: HTTPException):
        return jsonify(error=e.name, message=e.description), e.code

    @app.errorhandler(422)
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error="Bad Request", message=getattr(e, "description", "Invalid input")), 400

    @app.errorhandler(Exception)
    def unhandled(e):
        app.logger.exception(e)
        return jsonify(error="Internal Server Error", message="Something went wrong"), 500
