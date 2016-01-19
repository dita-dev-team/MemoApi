from flask.ext.restful import Resource, abort
from flask.ext.restful.reqparse import RequestParser
from api import bcrypt
from api.models import User, Individual, Group

parser = RequestParser()
parser.add_argument("username", type=str, help="A username is required", required=True, location="form")
parser.add_argument("email", type=str, help="An email is required", required=True, location="form")
parser.add_argument("password", type=str, help="A password is required", required=True, location="form")
parser.add_argument("type", type=str, help="A user type is required", required=True, location="form")
auth_parser = parser.copy()
auth_parser.remove_argument("type")


class UserApi(Resource):
    def get(self, username=None):
        response = {}
        if username:
            user = User.objects(username__iexact=username).first()

            if not user:
                abort(404, message="Username does not exist.")

            response = {
                'username': user.username,
                'email': user.email,
                'type': user.user_type,
                'created_at': str(user.created_at),
                'updated_at': str(user.updated_at)
            }
        else:
            users = User.objects()

            for index, user in enumerate(users):
                response[index + 1] = {
                    'username': user.username,
                    'email': user.email,
                    'type': user.user_type,
                    'created_at': str(user.created_at),
                    'updated_at': str(user.updated_at)
                }

        return response

    def post(self):
        args = parser.parse_args()

        user = User.objects(username__iexact=args['username']).first()
        if user:
            abort(409, message="Username already exists.")

        user = User(username=args['username'])
        user.password = bcrypt.generate_password_hash(args['password'])

        if args['type'] == 'individual':
            user.user_type = args['type']
            user.user_profile = Individual()
        elif args['type'] == 'group':
            user.user_type = args['type']
            user.user_profile = Group()

        user.save()

        response = {
            'username': user.username,
            'email': user.email,
            'type': user.user_type,
            'created_at': str(user.created_at),
            'updated_at': str(user.updated_at)
        }

        return response

    def put(self, username):
        if not username:
            abort(404, message="A username is required.")

        args = auth_parser.parse_args()
        user = User.objects(username__iexact=username).first()

        if not user:
            abort(404, message="Username does not exist.")

        user.password = bcrypt.generate_password_hash(args['password'])

        user.save()

        response = {
            'username': user.username,
            'email': user.email,
            'type': user.user_type,
            'created_at': str(user.created_at),
            'updated_at': str(user.updated_at)
        }

        return response

    def delete(self, username):
        if not username:
            abort(404, message="A username is required.")

        user = User.objects(username__iexact=username).first()
        if not user:
            abort(404, message="Username does not exist.")

        user.delete()

        response = {'message': 'deleted'}

        return response


class UserAuthentication(Resource):
    def post(self):
        args = auth_parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.objects(username__iexact=username).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                return {'Success': 'User authenticated.'}

        return {'Error': 'Invalid username or password.'}, 401


class UserProfileApi(Resource):
    def get(self, username):
        if not username:
            abort(404, message="A username is required.")

        user = User.objects(username__iexact=username).first()

        if not user:
            abort(404, message="Username does not exist.")

        if user.user_type == 'individual':
            pass
        else:
            pass


    def put(self, username):
        pass