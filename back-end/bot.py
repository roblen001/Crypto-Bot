from csv import writer
import pandas as pd
import websocket
import json
import pprint
import talib
import numpy
import config
import os
from binance.client import Client
from binance.enums import *

# TODO: once a transaction is succesfully completed we want to make an api call
#  - get future account transaction history list
#  - the assumption is that it this history will be completed when the transaction is succesful (function get_all_orders)

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

#  setting up the test network
test_api = config.TEST_API_KEY
test_secret = config.TEST_SECRET_KEY
client = Client(test_api, test_secret)
client.API_URL = 'https://testnet.binance.vision/api'

#  GET ACCOUNT BALANCES
# account = client.get_account()
# balances = account['balances']
# print(balances)

# CALCULATING TOTAL PROFITS ON A TRADE
# (selling_price - (selling_price*0.075))-(buying_price - (buying_price*0.075)) = profits in amount
# (selling_price - (selling_price*0.075))/(buying_price - (buying_price*0.075))*100 = profits in percent


# BUY A CURRENCY
#  market order:A market order is an order to buy or sell a security immediately.
#   This type of order guarantees that the order will be executed, but does not guarantee the execution price.
#  A market order generally will execute at or near the current bid (for a sell order) or ask (for a buy order) price.

#  STORING TRANSACTION TO DATABASE AND BUY CRYPTO


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


# order = client.create_order(
#     symbol='LTCBTC',
#     side='BUY',
#     type='MARKET',
#     quantity=3)

order = {
    "symbol": "LTCUSDT",
    "orderId": 28,
    "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
    "transactTime": 1507725176595,
    "price": "0.00000000",
    "origQty": "10.00000000",
    "executedQty": "10.00000000",
    "status": "FILLED",
    "timeInForce": "GTC",
    "type": "MARKET",
    "side": "SELL",
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
cum_market_price = market_price*qty
#  might need to be adjusted later
fee_percent = 0.075/100
fee = cum_market_price*fee_percent
# assumption is that fills['price'] includes fees, but to be safe we do this
price_with_fee = cum_market_price + fee

if side == 'BUY':
    profits = '---'
    profits_percent = '---'
else:
    df = pd.read_csv("../transaction_history.csv")
    reversed_data = df.iloc[::-1]
    df_funnel = df.loc[(df['symbol'] == symbol) & (df['side'] == 'BUY')]
    df_funnel['timestamp'] = pd.to_datetime(
        df_funnel.timestamp, unit='ms')
    df_funnel_most_recent_date = df_funnel.max()
    buy_price = df_funnel_most_recent_date['price_with_fee']
    profits = price_with_fee - buy_price
    profits_percent = (profits/buy_price)*100

order_list = [id, symbol, market_price, qty, timestamp, side,
              cum_market_price, fee, fee_percent, price_with_fee, profits, profits_percent]
print(order_list)

append_list_as_row("../transaction_history.csv", order_list)

# print(complete_trade_history)
# closes = []
# # WARNING THIS IS FOR REAL NETWORK
# # client = Client(config.API_KEY, config.API_SECRET, tld='us')


# def on_open(ws):
#     print('opened connection')

# # TODO: send notifications if connection closes
#     #  -it means that the server crashed and the bot is no longer running


# def on_close(ws):
#     print('closed connection')


# def on_message(ws, message):
#     global closes

#     # print('received message')
#     json_message = json.loads(message)
#     # pprint.pprint(json_message)

#     candle = json_message['k']

#     is_candle_closed = candle['x']
#     close = candle['c']

#     if is_candle_closed:
#         print("candle closed at {}".format(close))
#         closes.append(float(close))
#         print("closes")
#         print(closes)


# ws = websocket.WebSocketApp(SOCKET, on_open=on_open,
#                             on_close=on_close, on_message=on_message)
# ws.run_forever()
