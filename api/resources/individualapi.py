from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from api import bcrypt
from api.models import Individual
from api.resources.utilities import auth_parser, group_member_processes
from api.validators import validate_client, validate_file, validate_id_no


def student_id_no(value):
    if not validate_id_no(value):
        raise ValueError("Invalid id number. Id number must be of type xx-xxxx")

    return value

parser = RequestParser()
parser.add_argument("id_no", type=student_id_no, help="An id number is required", required=True, location="form")
parser.add_argument("name", type=str, location="form")
parser.add_argument("password", type=str, help="A password is required", required=True, location="form")
parser.add_argument("image", type=FileStorage, location="files")


class IndividualApi(Resource):
    method_decorators = [validate_client]

    def get(self, id_no=None):
        response = {}
        if id_no:
            individual = Individual.objects(id_no=id_no).first()

            if not individual:
                abort(404, message="An individual with that id number does not exist.")

            response = {
                'id_no': individual.id_no,
                'name': individual.name,
                'image': str(individual.image.grid_id) if individual.image.grid_id else None
            }
        else:
            individuals = Individual.objects()
            for individual in individuals:
                response[individual.id_no] = {
                    'name': individual.name,
                    'image': str(individual.image.grid_id) if individual.image.grid_id else None

                }

        return response

    def post(self):
        args = parser.parse_args()
        individual = Individual.objects(id_no=args['id_no']).first()
        if individual:
            abort(409, message="An individual with that id number already exists.")

        individual = Individual(id_no=args['id_no'], name=args['name'])
        individual.password = bcrypt.generate_password_hash(args['password'])

        if args['image'] and validate_file(args['image'].filename):
            individual.image.put(args['image'], content_type=args['image'].content_type)

        individual.save()

        response = {
            'id_no': individual.id_no,
            'name': individual.name,
            'image': str(individual.image.grid_id) if individual.image.grid_id else None
        }

        return response, 201

    def put(self, id_no=None):
        if not id_no:
            abort(404, message="An id number is required.")

        args = parser.parse_args()
        individual = Individual.objects(id_no=id_no).first()

        if not individual:
            abort(404, message="An individual with that id number does not exist.")

        individual.name = args['name']

        if args['image'] and validate_file(args['image'].filename):
            if individual.image:
                individual.image.replace(args['image'], content_type=args['image'].content_type)
            else:
                individual.image.put(args['image'], content_type=args['image'].content_type)

        response = {
            'id_no': individual.id_no,
            'name': individual.name,
            'image': str(individual.image.grid_id) if individual.image.grid_id else None
        }

        individual.save()

        return response

    def delete(self, id_no=None):
        if not id_no:
            abort(404, message="An id number is required.")

        individual = Individual.objects(id_no=id_no).first()

        if not individual:
            abort(404, message="An individual with that id number does not exist.")

        if individual.image:
            individual.image.delete()

        individual.delete()

        return {'success': "Individual successfully deleted."}


class IndividualGroupsApi(Resource):
    method_decorators = [validate_client]

    def get(self, id_no=None):
        if not id_no:
            abort(404, message="An id number is required.")

        individual = Individual.objects(id_no=id_no).first()

        if not individual:
            abort(404, message="An individual with that id number does not exist.")

        response = {'groups': {}}
        if individual.groups:
            for group in individual.groups:
                response['groups'][group.name] = {
                    'name': group.full_name,
                }

        return response

    def post(self, id_no=None, name=None):
        group_member_processes('insert', id_no, name)
        return {'Success': 'Group added successfully'}

    def delete(self, id_no=None, name=None):
        group_member_processes('delete', id_no, name)
        return {'Success': 'Group removed successfully'}


class IndividualAuthentication(Resource):
    method_decorators = [validate_client]

    def post(self):
        args = auth_parser.parse_args()
        id_no = args['username']
        password = args['password']
        individual = Individual.objects(id_no=id_no).first()

        if individual:
            if bcrypt.check_password_hash(individual.password, password):
                return {'Success': 'Individual has been successfully authenticated.'}

        return {'Error': 'Invalid username or password.'}, 401
