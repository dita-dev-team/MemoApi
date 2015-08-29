from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "memo"}
api = Api(app)
db = MongoEngine(app)

import api.views
