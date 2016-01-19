from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
from flask_restful import Api

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
app.config['TESTING'] = True
app.config['MONGODB_SETTINGS'] = {'DB': "memo_test"}
# app.config['MONGODB_SETTINGS'] = {'DB': "memo"}
rest_api = Api(app, '/api/v1')
bcrypt = Bcrypt(app)
db = MongoEngine(app)

import api.errors
import api.resources
