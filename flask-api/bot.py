import websocket
import json
import pprint
import numpy
import config
from binance.client import Client
from binance.enums import *
from csv import writer
import pandas as pd
import smtplib
import matplotlib.pyplot as plt
from getData import get_data_onStart
import csv
from tradingview_ta import TA_Handler, Interval, Exchange


SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

#  setting up the test network
test_api = config.TEST_API_KEY
test_secret = config.TEST_SECRET_KEY
client = Client(test_api, test_secret)
client.API_URL = 'https://testnet.binance.vision/api'

TRADE_SYMBOL = 'ETHUSDT'
# TODO: create a function to be the max possible amount
TRADE_QUANTITY = 0.05

# send notification email


def send_mail(content):
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(config.DEV_EMAIL, config.EMAIL_PASS)

    mail.sendmail(config.DEV_EMAIL,
                  config.PERSONAL_EMAIL, content)

    mail.close()

# helper function to append to csv


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


# buying/selling the crypto
# TODO: when buying send a notification

def order(side, quantity, symbol, order_type='MARKET'):
    try:
        print("sending order")
        # order = client.create_order(
        #     symbol=symbol, side=side, type=order_type, quantity=quantity)

        id = order['clientOrderId']

        symbol = order['symbol']
        market_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        qty = float(order['fills'][0]['qty'])
        timestamp = order['transactTime']
        side = order['side']
        cum_market_price = market_price*qty
        #  might need to be adjusted later
        fee_percent = 0.075
        fee = cum_market_price*fee_percent
        # assumption is that fills['price'] includes fees, but to be safe we do this
        #  I believe this works if were buying based on quantity
        price_with_fee = cum_market_price + fee

        if side == 'BUY':
            # TODO: this should be NAs not ---
            profits = '---'
            profits_percent = '---'
        else:
            df = pd.read_csv("../transaction_history.csv")
            reversed_data = df.iloc[::-1]
            df_funnel = df.loc[(df['symbol'] == symbol)
                               & (df['side'] == 'BUY')]
            df_funnel['timestamp'] = pd.to_datetime(
                df_funnel.timestamp, unit='ms')
            df_funnel_most_recent_date = df_funnel.max()
            buy_price = df_funnel_most_recent_date['price_with_fee']
            profits = price_with_fee - buy_price
            profits_percent = (profits/buy_price)*100

        order_list = [id, symbol, market_price, qty, timestamp, side,
                      cum_market_price, fee, fee_percent, price_with_fee, profits, profits_percent]

        append_list_as_row("../transaction_history.csv", order_list)

    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def on_open(ws):
    get_data_onStart()
    send_mail('The bot is online and trading.')
    print('bot.py online')

# TODO: if connection closes send me a notification


def on_close(ws):
    send_mail('Server has been closed. The bot is no longer able to trade.')
    print('closed connection')


def on_message(ws, message):
    # print('received message')
    json_message = json.loads(message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        eth = TA_Handler(
            symbol="ETHUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_HOUR
        )
        indicator = eth.get_analysis().summary['RECOMMENDATION']
        print(eth.get_analysis().summary)
        if indicator == 'SELL' or indicator == 'STRONG_SELL':
            # TODO: -this will be flawed when I need to switch the bot currency
            df = pd.read_csv("../transaction_history.csv")
            limited_data = df.tail(10).iloc[::-1]
            # not in position need to sell
            if limited_data[-1]['side'] == "BUY":
                # put binance sell logic here
                order_succeeded = order(
                    'SELL', TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    send_mail('The bot has sold.')

        if indicator == 'BUY' or indicator == 'STRONG_BUY':
            if limited_data[-1]['side'] == "SELL":
                print('in')
                # put binance buy order logic here
                order_succeeded = order(
                    'BUY', TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    send_mail('The bot has bought.')


def bot():
    SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

    ws = websocket.WebSocketApp(SOCKET, on_open=on_open,
                                on_close=on_close, on_message=on_message)

    ws.run_forever()
