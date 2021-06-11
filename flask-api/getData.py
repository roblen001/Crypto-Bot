import matplotlib.pyplot as plt
import csv
from binance.client import Client
import config
from binance.enums import *
from datetime import date, datetime
import time
import pandas as pd
import os
import numpy as np

client = Client(config.API_KEY, config.API_SECRET)

#  this will only be ran to get the data if the server crashes


def get_data_onStart():
    # from the last data point selected we update the data
    # then we start the stream
    file = '../ETH_hourly_data.csv'
    # if data file exists delet it and re fetch the data
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")

    # today = date.today().strftime('%Y-%m-%d')
    # TODO: this only needs to go back like 50 days max for now
    # candlesticks = client.get_historical_klines(
    #     "ETHUSDT", Client.KLINE_INTERVAL_1HOUR, 'April 1 2021')
    candlesticks = client.get_historical_klines(
        "ETHUSDT", Client.KLINE_INTERVAL_1DAY, 'January 1 2020')

    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {
            "time": data[0]/1000,
            # "open": data[1],
            # "high": data[2],
            # "low": data[3],
            "close": data[4],
        }
        processed_candlesticks.append(candlestick)

    df = pd.DataFrame(processed_candlesticks)
    # TODO: remove or add the SMA
    # create 50 days simple moving average column
    # df['20_SMA'] = df['close'].rolling(window=15, min_periods=1).mean()
    # # display first few rows
    # df['45_SMA'] = df['close'].rolling(
    #     window=30, min_periods=1).mean()

    df.to_csv(
        '../ETH_hourly_data.csv', index=False)


# # plotting
# get_data_onStart()
# data = pd.read_csv("../ETH_hourly_data.csv")
# data['Signal'] = 0.0
# data['Signal'] = np.where(data['20_SMA'] > data['45_SMA'], 1.0, 0.0)
# data['Position'] = data['Signal'].shift(-1) - data['Signal']
# plt.figure(figsize=(20, 10))
# # plot close price, short-term and long-term moving averages
# data['close'].plot(color='k', label='Close Price')
# data['20_SMA'].plot(color='b', label='20-day SMA')
# # plot ‘buy’ signals
# data['45_SMA'].plot(color='g', label='45-day SMA')
# plt.plot(data[data['Position'] == 1].index,
#          data['20_SMA'][data['Position'] == 1],
#          '^', markersize=15, color='g', label='buy')
# # plot ‘sell’ signals
# plt.plot(data[data['Position'] == -1].index,
#          data['20_SMA'][data['Position'] == -1],
#          'v', markersize=15, color='r', label='sell')
# plt.ylabel('Price in dollars', fontsize=15)
# plt.xlabel('Date', fontsize=15)
# plt.title('ETHUSDT', fontsize=20)
# plt.legend()
# plt.grid()
# plt.show()
