"""
Flask app for the trading agent. These are the backend components for the front-end folder 
where the trading dashboard interface is located.
"""
from pathlib import Path
import sys

import pandas as pd
from flask import jsonify
from flask_restful import Resource
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root / 'src'))

import pandas as pd
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from csv import DictWriter
import subprocess
from data_handler.crypto_news_scraper import CryptoNewsScraper
from trading_bot.trading_bot import bot
import configs.config
import nltk 

nltk.download('vader_lexicon')

# Initialize Flask app
app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS

@app.route("/")
def home():
    return "Trading Bot flask app is successfully running."

# Function to run a script as a subprocess
def run_script(script_name):
    # Run the subprocess
    print(f'Starting subprocess for {script_name}...')
    process = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(f'Subprocess for {script_name} started, now reading its output...')

# Start background tasks
run_script("app/run_top_news_scraper.py")
run_script("app/run_all_news_scraper.py")
run_script("app/run_trading_bot.py")

class AllTransactionHistory(Resource):
    def get(self, limit):
        """Fetch the transaction history with a limit."""
        df = pd.read_csv("/app/output_data/transaction_history.csv")
        limited_data = df.tail(limit).iloc[::-1]
        parsed = limited_data.to_dict(orient="records")
        return parsed

api.add_resource(AllTransactionHistory, "/all_transaction_history/<int:limit>")

class News(Resource):
    def get(self, type_, limit):
        """Fetch news articles based on type and limit."""
        path = f'/app/output_data/{type_}News.csv'
        df = pd.read_csv(path)
        
        # Ensure the DataFrame has the correct columns
        if df.shape[1] != 4:
            return jsonify({"error": "CSV file format is incorrect. Expected columns: title, link, date, article"}), 400
        
        df.fillna("Empty", inplace=True)
        
        # Initialize the sentiment analyzer
        sia = SentimentIntensityAnalyzer()
        
        # Define the function to get sentiment from the article
        def get_sentiment(article):
            sentiment_score = sia.polarity_scores(article)
            if sentiment_score['compound'] >= 0.05:
                return "Positive"
            elif sentiment_score['compound'] <= -0.05:
                return "Negative"
            else:
                return "Neutral"
        
        # Add a sentiment column to the DataFrame
        df['sentiment'] = df['article'].apply(get_sentiment)
        
        limited_data = df.tail(limit).iloc[::-1]
        parsed = jsonify(limited_data.to_dict(orient="records"))
        
        return parsed

api.add_resource(News, "/news/<string:type_>/<int:limit>")

class BotStatistics(Resource):
    def get(self, type):
        """Calculate bot statistics based on type.
        
        Class DEPRECATED because binance is banned in Canada.

        I will use mock data just to keep the front end up and running
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
            df = pd.read_csv('app/output_data/feedingHistoryData.csv')
            limited_data = df.tail(limit).iloc[::-1]
            result = limited_data.to_dict(orient="records")
        elif type == 'totalFed':
            df = pd.read_csv('app/output_data/feedingHistoryData.csv')
            result = int(df['amount'].sum())
        return result

api.add_resource(BotFeeder, "/botfeeder/<string:type>/<int:limit>")

class BotFeederAddData(Resource):
    def post(self):
        """Add data to the feeding history."""
        with open('app/output_data/feedingHistoryData.csv', 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=['amount', 'timestamp'])
            dictwriter_object.writerow(request.get_json(force=True))
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
