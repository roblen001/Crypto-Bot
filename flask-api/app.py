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
# custom functions

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


class BotStatistics(Resource):
    # this will calculate all the overall bot statistics
    # TODO: tie up to SQL database
    def get(self, type):
        result = 0
        df = pd.read_csv("../transaction_history.csv")
        if type == 'netprofits':
            for symbol in df['symbol'].unique():
                # finding the first buying price ever of the symbol
                df_funnel = df.loc[(df['symbol'] == symbol)
                                   & (df['side'] == 'BUY')]
                first_buy = df_funnel.head(1)['price_with_fee']
                current_market_price = 1
                potential_profits = current_market_price - first_buy
            totalProfit = 2
            sellData = df.loc[df['side'] == 'SELL']
            toNumeric = pd.to_numeric(
                sellData['profits'])
            botProfit = toNumeric.sum()
            result = toNumeric.sum()
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

if __name__ == "__main__":
    app.run(debug=True)
