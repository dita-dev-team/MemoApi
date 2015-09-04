from flask import jsonify
from api import app

ERROR_500 = {
    'Error': 'An internal error has occurred.\nPlease report this issue and it will be fixed as soon as possible.'
}

@app.errorhandler(TypeError)
def type_error(e):
    return jsonify(ERROR_500)

@app.errorhandler(KeyError)
def type_error(e):
    return jsonify(ERROR_500)


@app.errorhandler(500)
def internal_error(e):
    return jsonify(ERROR_500)