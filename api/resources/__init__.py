from api import rest_api
from api.resources.groupapi import GroupApi, GroupByImageApi, GroupByMembersApi
from api.resources.individualapi import IndividualApi, IndividualByGroupsApi

rest_api.add_resource(GroupApi, '/api/groups', '/api/groups/', '/api/groups/<string:name>')
rest_api.add_resource(GroupByImageApi, '/api/groups/images', '/api/groups/images/', '/api/groups/images/<string:image>')
rest_api.add_resource(GroupByMembersApi, '/api/groups/<string:name>/members', '/api/groups/<string:name>/members/',
                      '/api/groups/<string:name>/members/<string:id_no>')

rest_api.add_resource(IndividualApi, '/api/individuals', '/api/individuals/', '/api/individuals/<string:id_no>')
rest_api.add_resource(IndividualByGroupsApi, '/api/individuals/<string:id_no>/groups',
                      '/api/individuals/<string:id_no>/groups', '/api/individuals/<string:id_no>/groups/<string:name>')


