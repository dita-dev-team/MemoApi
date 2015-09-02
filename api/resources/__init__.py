from api import rest_api
from api.resources.groupapi import GroupApi

rest_api.add_resource(GroupApi, '/api/groups', '/api/groups/', '/api/groups/<string:name>',
                      '/api/groups/f/<string:specifier>', '/api/groups/f/<string:specifier>/',
                      '/api/groups/f/<string:specifier>/<string:value>')


