from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

parser = RequestParser()
parser.add_argument("name", type=str, help="A name is required", required=True, location="form")
parser.add_argument("full_name", type=str, location="form")
parser.add_argument("image", type=FileStorage, location="files")


class GroupView(Resource):

    def get(self, name=None):
        if name:
            return {'get': 'This is a get request %s' % name}
        else:
            return {'get': 'This is a get request'}

    def post(self):
        args = parser.parse_args()
        response = {
            'name': args['name'],
            'full_name': args['full_name'],
            'image': args['image'].filename if args['image'] else None
        }

        return response, 201

    def put(self, name):
        pass

    def delete(self, name):
        pass
