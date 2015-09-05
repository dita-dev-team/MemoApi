from api import db
from api.validators import validate_client
from bson import ObjectId
from bson.errors import InvalidId
from flask import send_file
from flask_restful import abort, Resource
from gridfs.errors import NoFile

class Images(Resource):
    method_decorators = [validate_client]
    
    def get(self, oid=None):
        if not oid:
            abort(404, message="A valid image id is required.")

        try:
            fs = db.GridFSProxy(ObjectId(oid))
            image = fs.get()
        except InvalidId or NoFile:
            abort(404, message="The requested image was not found.")

        return send_file(image, mimetype=image.content_type)