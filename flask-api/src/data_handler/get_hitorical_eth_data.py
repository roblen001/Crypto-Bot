"""
WARNING: This script is DEPRECATED due to the Binance trading platform no longer working in Canada.

File to fetch and process historical ETH data.
"""

import matplotlib.pyplot as plt
import csv
# from binance.client import Client
import configs.config
# from binance.enums import *
from datetime import date, datetime
import time
import pandas as pd
import os
import numpy as np

# client = Client(config.API_KEY, config.API_SECRET)

def get_data_onStart():
    """
    Fetch historical ETH data and save it to a CSV file.

    This function is run to get the data if the server crashes.
    It deletes any existing data file and re-fetches the data from Binance.
    """
    raise DeprecationWarning('Binance is banned in Canada.')
    file = '../ETH_hourly_data.csv'

    # If data file exists, delete it and re-fetch the data
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")

    # Fetch historical candlestick data from Binance
    candlesticks = client.get_historical_klines(
        "ETHUSDT", Client.KLINE_INTERVAL_1DAY, 'January 1 2020')

    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "close": data[4],
        }
        processed_candlesticks.append(candlestick)

    df = pd.DataFrame(processed_candlesticks)

    # Save the data to a CSV file
    df.to_csv('../ETH_hourly_data.csv', index=False)

def plot_binance_data():
    """Plot binance data
    """
    data = pd.read_csv("../ETH_hourly_data.csv")
    data['Signal'] = 0.0
    data['Signal'] = np.where(data['20_SMA'] > data['45_SMA'], 1.0, 0.0)
    data['Position'] = data['Signal'].shift(-1) - data['Signal']
    plt.figure(figsize=(20, 10))
    data['close'].plot(color='k', label='Close Price')
    data['20_SMA'].plot(color='b', label='20-day SMA')
    data['45_SMA'].plot(color='g', label='45-day SMA')
    plt.plot(data[data['Position'] == 1].index, data['20_SMA'][data['Position'] == 1], '^', markersize=15, color='g', label='buy')
    plt.plot(data[data['Position'] == -1].index, data['20_SMA'][data['Position'] == -1], 'v', markersize=15, color='r', label='sell')
    plt.ylabel('Price in dollars', fontsize=15)
    plt.xlabel('Date', fontsize=15)
    plt.title('ETHUSDT', fontsize=20)
    plt.legend()
    plt.grid()
    plt.show()
