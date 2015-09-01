from api import api
from api.resources.groupapi import GroupApi

api.add_resource(GroupApi,
                 '/api/groups',
                 '/api/groups/',
                 '/api/groups/<string:name>')