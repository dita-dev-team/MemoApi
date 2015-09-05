from api.models import Group, Individual
from flask_restful import abort
from flask_restful.reqparse import RequestParser


auth_parser = RequestParser()
auth_parser.add_argument("username", type=str, help="A username is required", required=True, location="form")
auth_parser.add_argument("password", type=str, help="A password is required", required=True, location="form")


def group_member_processes(process, member_id_no=None, group_name=None):
    if not member_id_no:
        abort(404, message="An id number is required.")

    if not group_name:
        abort(404, message="A group name is required.")

    individual = Individual.objects(id_no=member_id_no).first()
    group = Group.objects(name__iexact=group_name).first()

    if not individual:
        abort(404, message="An individual with that id number does not exist.")

    if not group:
        abort(404, message="A group with that name does not exist.")

    if process == 'insert':
        individual.update(add_to_set__groups=[group])
        group.update(add_to_set__members=[individual])
    elif process == 'delete':
        individual.update(pull__groups=group)
        group.update(pull__members=individual)
