from os import environ

from flask import Flask
from flask_restful import Api

from resources import Stars, List

app = Flask(__name__)
api = Api(app)

api.add_resource(Stars, '/stars')
api.add_resource(List, '/list')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=environ.get('flask_debug', False))
