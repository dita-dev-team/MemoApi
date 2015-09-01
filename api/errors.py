from flask import jsonify
from api import app

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'Error': 'An internal error has occurred. Please report this issue and it will be'
                 'fixed as soon as possible.'
    })