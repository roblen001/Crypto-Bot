'''This is a custom cryptocurrency trading environment created with
    openAi gym.

    author: Roberto Lentini
    email: roberto.lentini@mail.utoronto.ca
    date: November 22nd 2021
'''
import gym
from gym import spaces
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import static


class CryptoEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, data, title=None):
        super(CryptoEnv, self).__init__()
        # initializing account and historical data
        self.data = data
        # THIS FEELS USELESS, TRY AND REMOVE THIS GARBAGE
        # self.reward_range = (-static.MAX_ACCOUNT_BALANCE,
        #                      static.MAX_ACCOUNT_BALANCE)
        self.total_fees_paid = 0
        self.total_volume_traded = 0
        self.crypto_held = 0
        # TODO: this also feels useless
        self.bnb_usdt_held = static.BNBUSDTHELD
        self.bnb_usdt_held_start = static.BNBUSDTHELD
        self.current_episode = 1
        # initializing list to store information for graphing purposes
        self.graph_reward = []
        self.graph_profit = []
        # the trading agent's goal is to beat the benchmark (which will
        # be the buy and hold method). It doesnt bring us anything to just
        # make money because the agent will make money if crypto price has
        # a gain. Thus the goal is to beat the benchmark (current strategy.)
        self.graph_benchmark = []
        self.action_space = spaces.Discrete(
            low=-1, high=1, shape=(1,), dtype=np.float16)
        # initializing observation space
        # TODO: this will need to contain all of the gathered data not just prices
        # TODO: confirm if shape is for a single candle
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(10, 5), dtype=np.float16)

    def step(self, action):
        ...
        return observation, reward, done, info

    def reset(self):
        ...
        return observation  # reward, done, info can't be included

    def render(self, mode='human'):
        ...

    def close(self):
        ...
