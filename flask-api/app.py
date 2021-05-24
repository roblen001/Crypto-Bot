from flask import Flask, jsonify, request
from flask_restful import Api, Resource
# import websocket
import json
import pprint
import config
import os
from binance.client import Client
from binance.enums import *
import pandas as pd
import requests
from csv import DictWriter
from flask_cors import CORS
# custom functions

test_api = config.TEST_API_KEY
test_secret = config.TEST_SECRET_KEY
client = Client(test_api, test_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# env\Scripts\activate
app = Flask(__name__)
api = Api(app)
# check options for this for security reasons
CORS(app)


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


class BotStatistics(Resource):
    # this will calculate all the overall bot statistics
    # TODO: tie up to SQL database
    def get(self, type):
        result = 0
        df = pd.read_csv("../transaction_history.csv")
        if type == 'netprofits':
            # assuming account balance is in quantity
            total_assets_value = 0
            for symbol in client.get_account()['balances']:
                asset_ticker = symbol['asset'] + 'USDT'
                asset_quantity = symbol['free']
                # print(symbol['asset'])
                # print(symbol['free'])
                # market_prices = client.get_symbol_ticker()
                if symbol['asset'] != 'USDT':
                    response = requests.get(
                        "https://api.binance.com/api/v1/ticker/price?symbol=" + asset_ticker)
                    symbol_marketPrice = response.json()['price']
                    total_assets_value += float(symbol_marketPrice) * \
                        float(asset_quantity)
                if symbol['asset'] == 'USDT':
                    total_assets_value += float(asset_quantity)
            df = pd.read_csv('../feedingHistoryData.csv')
            totalFed = int(df['amount'].sum())
            result = total_assets_value - totalFed
        elif type == 'positivetrades':
            sellData = df.loc[df['side'] == 'SELL']
            totalCountSellTransactions = len(sellData['profits'])
            toNumeric = pd.to_numeric(
                sellData['profits'])
            countPositiveTrades = len(toNumeric.loc[toNumeric >= 0])
            result = countPositiveTrades/totalCountSellTransactions * 100
        elif type == 'comparestrategy':
            sellData = df.loc[df['side'] == 'SELL']
            toNumeric = pd.to_numeric(
                sellData['profits'])
            result = toNumeric.sum()

        return result


# determining the root of the resource
api.add_resource(BotStatistics,
                 "/botstatistics/<string:type>")


class BotFeeder(Resource):
    # keeps track of the amount of money user is inputing into the bot
    # user keeps track of this manually
    def get(self, type, limit):
        if type == 'feedingHistoryData':
            df = pd.read_csv('../feedingHistoryData.csv')
            limited_data = df.tail(limit).iloc[::-1]
            result = limited_data.to_dict(orient="records")
        elif type == 'totalFed':
            df = pd.read_csv('../feedingHistoryData.csv')
            result = int(df['amount'].sum())
        return result


        # determining the root of the resource
api.add_resource(BotFeeder,
                 "/botfeeder/<string:type>/<int:limit>")


class BotFeederAddData(Resource):
    # when bot is fed data is added to the database
    def post(self):
        with open('../feedingHistoryData.csv', 'a') as f_object:

            # Pass the file object and a list
            # of column names to DictWriter()
            # You will get a object of DictWriter
            dictwriter_object = DictWriter(
                f_object, fieldnames=['amount', 'timestamp'])

            # Pass the dictionary as an argument to the Writerow()
            dictwriter_object.writerow(request.get_json(force=True))

            # Close the file object
            f_object.close()
        return 'data added'


        # determining the root of the resource
api.add_resource(BotFeederAddData,
                 "/botFeederAddData")


if __name__ == "__main__":
    app.run(debug=True)