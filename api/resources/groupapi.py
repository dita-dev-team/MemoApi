import re
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from api.model import Group
from api.resources.miscellaneous import group_member_processes
from api.validators import validate_client, validate_file

parser = RequestParser()
parser.add_argument("name", type=str, help="A name is required", required=True, location="form")
parser.add_argument("full_name", type=str, location="form")
parser.add_argument("image", type=FileStorage, location="files")


class GroupApi(Resource):
    method_decorators = [validate_client]

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

    def put(self, name=None):
        if not name:
            abort(404, message="A group name is required.")

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

    def delete(self, name=None):
        if not name:
            abort(404, message="A group name is required.")
        group = Group.objects(name__iexact=name).first()

        if not group:
            abort(404, message="A group with that name does not exist.")

        if group.image:
            group.image.delete()

        group.delete()

        return {'success': "Group successfully deleted."}


class GroupByFullNameApi(Resource):
    method_decorators = [validate_client]

    def get(self, fullname=None):
        group = Group.objects(full_name__iexact=fullname).first()

        if not group:
            abort(404, message="A group with that name does not exist.")

        response = {
            'name': group.name,
            'full_name': group.full_name,
            'image': str(group.image.grid_id) if group.image.grid_id else None
        }

        return response


class GroupByImageApi(Resource):
    method_decorators = [validate_client]

    def get(self, image=None):
        response = {}
        if image:
            print(image)
            groups = Group.objects(image=None)
        else:
            groups = Group.objects(image__ne=None)

        for group in groups:
            response[group.name] = {
                'full_name': group.full_name,
                'image': str(group.image.grid_id) if group.image.grid_id else None
                }

        return response


class GroupByMembersApi(Resource):
    method_decorators = [validate_client]

    def get(self, name=None):
        if not name:
            abort(404, message="A group name is required.")

        group = Group.objects(name__iexact=name).first()

        if not group:
            abort(404, message="A group with that name does not exist.")

        response = {'members': {}}
        if group.members:
            for member in group.members:
                response['members'][member.id_no] = {
                    'name': member.name,
                }

        return response

    def post(self, name=None, id_no=None):
        group_member_processes('insert', id_no, name)
        return {'Success': 'Individual added successfully'}

    def delete(self, name=None, id_no=None):
        group_member_processes('delete', id_no, name)
        return {'Success': 'Individual removed successfully'}
