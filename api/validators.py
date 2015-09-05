import re
from api import bcrypt
from flask_restful import abort, request
from functools import wraps

ALLOWED_CLIENTS = {
    'mobile': '$2a$12$zFe.yTBPFB4xfxkZfOiCp.je.i.QpNPESL0MqBdmguiY9hfcBnDt6',
    'native': '$2a$12$hauuuzh.HWfJZP3Gb8t.MeyS4LpsV6sW3zOoLChxToN5wGuLHotpy',
    'web': '$2a$12$mzNHeE.vZz.wFHJH7OKRqeOHUdtg9w5OHHOUUVzC54R5eHKJftRbW'
}
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def validate_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        if request.authorization:
            if bcrypt.check_password_hash(ALLOWED_CLIENTS[request.authorization['username']],
                                          request.authorization['password']):
                return func(*args, **kwargs)

        abort(401, message="Authorization is required")

    return wrapper


def validate_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def validate_id_no(id_no):
    result = re.search('\d\d\W\d\d\d\d', id_no)
    return result is not None

