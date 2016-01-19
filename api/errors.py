from flask import jsonify
from api import app

ERROR_404 = {
    'Error': 'The requested url was not found.'
}

ERROR_500 = {
    'Error': 'An internal error has occurred.\nPlease report this issue and it will be fixed as soon as possible.'
}


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(ERROR_404), 404


@app.errorhandler(TypeError)
def type_error(e):
    return jsonify(ERROR_500), 500


@app.errorhandler(KeyError)
def type_error(e):
    return jsonify(ERROR_500), 500


@app.errorhandler(500)
def internal_error(e):
    return jsonify(ERROR_500), 500