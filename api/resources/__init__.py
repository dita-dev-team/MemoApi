from api import rest_api
from api.resources.groupapi import GroupApi, GroupAuthentication, GroupImageApi, GroupMembersApi
from api.resources.individualapi import IndividualApi, IndividualAuthentication, IndividualGroupsApi
from api.resources.miscellaneousapi import Images
from api.resources.userapi import UserApi, UserAuthentication, UserProfileApi


"""rest_api.add_resource(GroupApi, '/groups', '/groups/', '/groups/<string:name>')
rest_api.add_resource(GroupImageApi, '/groups/images', '/groups/images/', '/groups/images/<string:image>')
rest_api.add_resource(GroupMembersApi, '/groups/<string:name>/members', '/groups/<string:name>/members/',
                      '/groups/<string:name>/members/<string:id_no>')
rest_api.add_resource(GroupAuthentication, '/api/groups/authenticate', '/api/groups/authenticate/')

rest_api.add_resource(IndividualApi, '/individuals', '/individuals/', '/individuals/<string:id_no>')
rest_api.add_resource(IndividualGroupsApi, '/individuals/<string:id_no>/groups',
                      '/individuals/<string:id_no>/groups/', '/individuals/<string:id_no>/groups/<string:name>')
rest_api.add_resource(IndividualAuthentication, '/individuals/authenticate', '/individuals/authenticate/')

rest_api.add_resource(Images, '/images/<string:oid>')"""

rest_api.add_resource(UserApi, '/users', '/users/', '/users/<string:username>')
rest_api.add_resource(UserAuthentication, '/users/authenticate', '/users/authenticate/')
rest_api.add_resource(UserProfileApi, '/users/profile/<string:username>')


