"""
Flask app for the trading agent. These are the backend components for the front-end floder 
where the trading dashboard interface is located.
"""

import pandas as pd
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from binance.client import Client
import requests
from csv import DictWriter
import time
import threading
from data_handler.crypto_news_scraper import CryptoNewsScraper
from trading_bot.trading_bot import bot
import configs.config
from multiprocessing import Process

# Initialize Binance client DEPRECATED Binance is banned in Canada
# api = config.API_KEY
# secret = config.API_SECRET
# client = Client(api, secret)

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS

# Background tasks
def run_top_news_scraper():
    """Scrapes top news every 30 minutes."""
    scraper = CryptoNewsScraper()
    while True:
        try:
            scraper.get_crypto_news('top')
            time.sleep(1800)
        except:
            # ADD CODE TO TERMINATE APP HERE
            raise RuntimeError('failed to start news scraper for top news')

def run_all_news_scraper():
    """Scrapes latest news every 15 minutes."""
    scraper = CryptoNewsScraper()
    while True:
        try:
            scraper.get_crypto_news('latest')
            time.sleep(900)
        except:
            # ADD CODE TO TERMINATE APP HERE
            raise RuntimeError('failed to start news scraper for latest news')

def trading_bot():
    """Runs the trading bot."""
    bot()

# Start background tasks
threading.Thread(target=run_top_news_scraper).start()
threading.Thread(target=run_all_news_scraper).start()
threading.Thread(target=trading_bot).start()

class AllTransactionHistory(Resource):
    def get(self, limit):
        """Fetch the transaction history with a limit."""
        df = pd.read_csv("../../output_data/transaction_history.csv")
        limited_data = df.tail(limit).iloc[::-1]
        parsed = limited_data.to_dict(orient="records")
        return parsed

api.add_resource(AllTransactionHistory, "/all_transaction_history/<int:limit>")

class News(Resource):
    def get(self, type, limit):
        """Fetch news articles based on type and limit."""
        path = f'../../output_data/{type}News.csv'
        df = pd.read_csv(path)
        limited_data = df.tail(limit).iloc[::-1]
        parsed = limited_data.to_dict(orient="records")
        return parsed

api.add_resource(News, "/news/<string:type>/<int:limit>")

class BotStatistics(Resource):
    def get(self, type):
        """Calculate bot statistics based on type.
        
        Class DEPRECATED because binance is banned in Canada.
        """
        raise DeprecationWarning('Binance is banned in Canada.')
    
        result = 0
        df = pd.read_csv("../transaction_history.csv")
        if type == 'netprofits':
            total_assets_value = 0
            for symbol in client.get_account()['balances']:
                asset_ticker = symbol['asset'] + 'USDT'
                asset_quantity = symbol['free']
                if symbol['asset'] != 'USDT' and symbol['free'] != '0.00000000' and symbol['free'] != '0.00':
                    response = requests.get(f"https://api.binance.com/api/v1/ticker/price?symbol={asset_ticker}")
                    symbol_marketPrice = response.json()['price']
                    total_assets_value += float(symbol_marketPrice) * float(asset_quantity)
                if symbol['asset'] == 'USDT':
                    total_assets_value += float(asset_quantity)
            df = pd.read_csv('../feedingHistoryData.csv')
            totalFed = int(df['amount'].sum())
            result = total_assets_value - totalFed
        elif type == 'positivetrades':
            sellData = df.loc[df['side'] == 'SELL']
            totalCountSellTransactions = len(sellData['profits'])
            toNumeric = pd.to_numeric(sellData['profits'])
            countPositiveTrades = len(toNumeric.loc[toNumeric >= 0])
            result = countPositiveTrades / totalCountSellTransactions * 100
        elif type == 'comparestrategy':
            sellData = df.loc[df['side'] == 'SELL']
            toNumeric = pd.to_numeric(sellData['profits'])
            result = str(toNumeric.sum())
        return result

api.add_resource(BotStatistics, "/botstatistics/<string:type>")

class BotFeeder(Resource):
    def get(self, type, limit):
        """Fetch feeding history data or total fed amount based on type and limit."""
        if type == 'feedingHistoryData':
            df = pd.read_csv('../../output_data/feedingHistoryData.csv')
            limited_data = df.tail(limit).iloc[::-1]
            result = limited_data.to_dict(orient="records")
        elif type == 'totalFed':
            df = pd.read_csv('../../output_data/feedingHistoryData.csv')
            result = int(df['amount'].sum())
        return result

api.add_resource(BotFeeder, "/botfeeder/<string:type>/<int:limit>")

class BotFeederAddData(Resource):
    def post(self):
        """Add data to the feeding history."""
        with open('../../output_data/feedingHistoryData.csv', 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=['amount', 'timestamp'])
            dictwriter_object.writerow(request.get_json(force=True))
            f_object.close()
        return 'data added'

api.add_resource(BotFeederAddData, "/botFeederAddData")

class GetBalance(Resource):
    def get(self):
        """Fetch the account balance.
        
        DEPRECATED Binance is banned in Canada
        """
        raise DeprecationWarning('Binance is banned in Canada.')
    
        balances = [symbol for symbol in client.get_account()['balances'] if symbol['free'] != '0.00000000' and symbol['free'] != '0.00']
        return balances

api.add_resource(GetBalance, "/getBalance")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
