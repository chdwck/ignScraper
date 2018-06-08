from flask import Flask, request
from flask_restful import Resource, Api
from database import DBController
import json

app = Flask(__name__)
api = Api(app)
dbc = DBController('ps4')

class Games(Resource):
    def get(self, console):
        dbc = DBController(console)
        data = dbc.compileList(console)
        dbc.close()
        return data

api.add_resource(Games, '/games/<console>')

if __name__ == '__main__':
    app.run(port='5002')
