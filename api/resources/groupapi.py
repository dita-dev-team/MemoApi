from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from api.model import Group
from api.validators import validate_file

parser = RequestParser()
parser.add_argument("name", type=str, help="A name is required", required=True, location="form")
parser.add_argument("full_name", type=str, location="form")
parser.add_argument("image", type=FileStorage, location="files")


class GroupApi(Resource):

    def get(self, name=None):
        response = {}
        if name:
            group = Group.objects(name__iexact=name).first()

            if not group:
                abort(404, message="A group with that name does not exist.")

            response = {
                'name': group.name,
                'full_name': group.full_name,
                'image': str(group.image.grid_id) if group.image.grid_id else None
            }
        else:
            groups = Group.objects()
            for group in groups:
                response[group.name] = {
                    'full_name': group.full_name,
                    'image': str(group.image.grid_id) if group.image.grid_id else None

                }

        return response

    def post(self):
        args = parser.parse_args()
        group = Group.objects(name__iexact=args['name']).first()
        if group:
            abort(409, message="A group with that name already exist.")

        group = Group(name=args['name'], full_name=args['full_name'])

        if args['image'] and validate_file(args['image'].filename):
            group.image.put(args['image'], content_type=args['image'].content_type)

        group.save()

        response = {
            'name': group.name,
            'full_name': group.full_name,
            'image': str(group.image.grid_id) if group.image.grid_id else None
        }

        return response, 201

    def put(self, name):
        args = parser.parse_args()
        group = Group.objects(name__iexact=name).first()

        if not group:
            abort(404, message="A group with that name does not exist.")

        group.full_name=args['full_name']

        if args['image'] and validate_file(args['image'].filename):
            if group.image:
                group.image.replace(args['image'], content_type=args['image'].content_type)
            else:
                group.image.put(args['image'], content_type=args['image'].content_type)

        response = {
            'name': group.name,
            'full_name': group.full_name,
            'image': str(group.image.grid_id) if group.image.grid_id else None
        }

        group.save()

        return response

    def delete(self, name):
        group = Group.objects(name__iexact=name).first()

        if not group:
            abort(404, message="A group with that name does not exist.")

        if group.image:
            group.image.delete()

        group.delete()

        return {'success': "Group successfully deleted."}
