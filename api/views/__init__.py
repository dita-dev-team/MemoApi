from api import api
from api.views.groupview import GroupView
from flask import Blueprint

api.add_resource(GroupView,
                 '/api/groups',
                 '/api/groups/',
                 '/api/groups/<string:name>')