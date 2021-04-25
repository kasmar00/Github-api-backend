from flask import Flask
from flask_restful import Api

from .resources import Stars, ListRep

# creating flask app and api
app = Flask(__name__)
api = Api(app)

# adding resources to api
api.add_resource(Stars, '/stars')
api.add_resource(ListRep, '/list')
