from flask import Flask, jsonify
from flask_restful import Api, Resource
# import websocket
import json
import pprint
import config
import os
from binance.client import Client
from binance.enums import *
import pandas as pd

test_api = config.TEST_API_KEY
test_secret = config.TEST_SECRET_KEY
client = Client(test_api, test_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# env\Scripts\activate
app = Flask(__name__)
api = Api(app)


class All_transaction_history(Resource):
    #  TODO:
    # -stored as sql but is converted to json()
    # -figured out what format to store the data
    def get(self, limit):
        df = pd.read_csv("../transaction_history.csv")
        limited_data = df.tail(limit).iloc[::-1]
        parsed = limited_data.to_dict(orient="records")

        return parsed


# determining the root of the resource
api.add_resource(All_transaction_history,
                 "/all_transaction_history/<int:limit>")


class News(Resource):
    # this will extract the top 10 articles from news database
    def get(self, type, limit):
        # TODO: -Make it clear that type can only be all or top
        path = '../' + type + 'News.csv'
        df = pd.read_csv(path)
        limited_data = df.tail(limit).iloc[::-1]
        parsed = limited_data.to_dict(orient="records")

        return parsed


# determining the root of the resource
api.add_resource(News,
                 "/news/<string:type>/<int:limit>")

if __name__ == "__main__":
    app.run(debug=True)
