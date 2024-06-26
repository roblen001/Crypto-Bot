"""
WARNING: This script is DEPRECATED due to the Binance trading platform no longer working in Canada.

File to run the trading bot using the Binance API. The different actions the bot can take are definied here.
This file also contains the logic for when to perform certain actions.

Author: Roberto Lentini
Email: roberto.lentini@mail.utoronto.ca
"""

import websocket
import json
import configs.config as config 
# from binance.client import Client
# from binance.enums import *
from csv import writer
import pandas as pd
import smtplib
import matplotlib.pyplot as plt
from data_handler.get_hitorical_eth_data import get_data_onStart
import requests
import time

# WebSocket for Binance data stream
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

# Setting up the Binance client
# api = config.API_KEY
# secret = config.API_SECRET
# client = Client(api, secret)

# uncomment to use rsi trading strategy but then you will need to 
# create a .env file with an API for https://api.taapi.io
# taapi = config.TAAPI

TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.05

def send_mail(content):
    """Send notification email."""
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(config.DEV_EMAIL, config.EMAIL_PASS)
    mail.sendmail(config.DEV_EMAIL, config.PERSONAL_EMAIL, content)
    mail.close()

def append_list_as_row(file_name, list_of_elem):
    """Append a list as a row to a CSV file."""
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def order(side, quantity, symbol, order_type='MARKET'):
    """Place an order on the Binance platform."""
    raise DeprecationWarning('Binance is no longer active in Canada.')
    try:
        print("sending order")
        order = {
            "symbol": symbol,
            "orderId": '28',
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": str(int(round(time.time() * 1000))),
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": side,
            "fills": [
                {
                    "price": "4000.00000000",
                    "qty": "1.00000000",
                    "commission": "4.00000000",
                    "commissionAsset": "USDT"
                },
            ]
        }

        id = order['clientOrderId']
        symbol = order['symbol']
        market_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        qty = float(order['fills'][0]['qty'])
        timestamp = order['transactTime']
        side = order['side']
        cum_market_price = market_price * qty
        fee_percent = 0.075
        fee = cum_market_price * (fee_percent / 100)
        price_with_fee = cum_market_price + fee

        if side == 'BUY':
            profits = '---'
            profits_percent = '---'
        else:
            df = pd.read_csv("../transaction_history.csv")
            df_funnel = df.loc[(df['symbol'] == symbol) & (df['side'] == 'BUY')]
            df_funnel['timestamp'] = pd.to_datetime(df_funnel.timestamp, unit='ms')
            df_funnel_most_recent_date = df_funnel.max()
            buy_price = df_funnel_most_recent_date['price_with_fee']
            profits = price_with_fee - buy_price
            profits_percent = (profits / buy_price) * 100

        order_list = [id, symbol, market_price, qty, timestamp, side,
                      cum_market_price, fee, fee_percent, price_with_fee, profits, profits_percent]

        append_list_as_row("../transaction_history.csv", order_list)

    except Exception as e:
        print(f"An exception occurred - {e}")
        return False

    return True

def on_open(ws):
    """Called when the WebSocket is opened."""
    get_data_onStart()
    send_mail('The bot is online and trading.')
    print('bot.py online')

def on_close(ws):
    """Called when the WebSocket is closed."""
    send_mail('Server has been closed. The bot is no longer able to trade.')
    print('closed connection')

def on_message(ws, message):
    """Called when a message is received from the WebSocket.
    
    This is the funciton where the trained model from: https://github.com/roblen001/reinforcement_learning_trading_agent
    can be added.

    TODO: might be worth making it easier for the user to integrate the trading bot into the system
    """
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        response = requests.get(f"https://api.taapi.io/rsi?secret={taapi}&exchange=binance&symbol=ETH/USDT&interval=1h")
        rsi = response.json()['value']
        print(rsi)

        if rsi > 75:
            df = pd.read_csv("../transaction_history.csv")
            limited_data = df.tail(10).iloc[::-1]
            if limited_data['side'].iloc[0] == "BUY":
                order_succeeded = order('SELL', TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    send_mail('The bot has sold.')

        if rsi < 35:
            df = pd.read_csv("../transaction_history.csv")
            limited_data = df.tail(10).iloc[::-1]
            if limited_data['side'].iloc[0] == "SELL":
                order_succeeded = order('BUY', TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    send_mail('The bot has bought.')

def bot():
    """Run the trading bot."""
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
