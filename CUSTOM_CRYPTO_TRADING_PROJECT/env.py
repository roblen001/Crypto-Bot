'''This is a custom cryptocurrency trading environment created with
    openAi gym.

    author: Roberto Lentini
    email: roberto.lentini@mail.utoronto.ca
    date: November 22nd 2021
'''
import matplotlib.pyplot as plt
import numpy as np
import gym
import random
from gym import spaces
import pandas as pd
# import static


class CryptoEnv(gym.env):
    def __init__(self, data, title=None):
        '''Initializing the enviroment variables

            - data: price data in csv format.
            - title: ????
        '''
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
        # initializing actions: buy: 1, hold: 0, sell: -1
        # we only buy and sell 100% of our assets
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(1,), dtype=np.float16)
        # initializing observation space
        # TODO: this will need to contain all of the gathered data not just prices
        # TODO: confirm if shape is for a single candle
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(10, 5), dtype=np.float16)

        def reset(self):
            '''Resets the environment after and episode.

                TODO: MIGHT BE AN IDEA TO ADD LATER ON
                - random_start = bool, if true on env reset the agent 
                    will start at random timepoint in the environment. If
                    False it will start at the starting point of data.

                Returns the next observation
            '''

            self.balance = static.INITIAL_ACCOUNT_BALANCE
            self.net_worth = static.INITIAL_ACCOUNT_BALANCE + static.BNBUSDTHELD
            self.total_fees_paid = 0
            # amount of the currency * the price of the currency
            self.total_volume_traded = 0
            self.crypto_held = 0
            # TODO: feels useless
            self.bnb_usdt_held = static.BNBUSDTHELD
            self.episode_reward = 0
            # set current step to be random point in dataframe
            # TODO: NEED TO BETTER UNDERSTANDING WHAT I AM DOING HERE
            start = list(range(4, len(self.data.loc[:, 'Open'].values)
                               - static.MAX_STEPS)) + self.data.index[0]
            # randomizing the weights for the first step
            weights = [i for i in start]
            self.current_step = random.choices(start, weights)[0]
            self.start_step = self.current_step

            return self._next_observation()

        def _next_observation(self):
            '''
            '''
            # Get the data for the last 5 timestep
            frame = np.array([
                self.df.loc[self.current_step - 4:self.current_step, 'Open'],
                self.df.loc[self.current_step - 4:self.current_step, 'High'],
                self.df.loc[self.current_step - 4:self.current_step, 'Low'],
                self.df.loc[self.current_step - 4:self.current_step, 'Close'],
                self.df.loc[self.current_step - 4:self.current_step, 'Volume'],
            ])
            obs = frame
            return obs

        def _take_action(self, action):
            '''Allows agent to buy and sell. Also caculates our net worth.

                - action: ??? a list of some kind
            '''

            # TODO: why is the current price being randomized between
            # open and closed, the decision should be consitantly made
            # on close. This is riducolous to add randomness to this process
            current_price = random.uniform(
                self.df.loc[self.current_step, 'Real open'],
                self.df.loc[self.current_step, 'Real close'])

            # BUY
            if action[0] > 0:
                # (by multiplying action to balance
                # we also check if we are in a position to buy)
                crypto_bought = self.balance * action[0] / current_price
                self.bnb_usdt_held -= crypto_bought * current_price * static.MAKER_FEE

                self.total_fees_paid += crypto_bought * current_price * static.MAKER_FEE
                self.total_volume_traded = crypto_bought * current_price
                self.balance -= crypto_bought * current_price
            # SELL
            if action[0] > 0:
                crypto_sold = -self.crypto_held * action[0]
                self.bnb_usdt_held -= crypto_sold * current_price * static.TAKER_FEE
                self.total_fees_paid += crypto_sold * current_price * static.TAKER_FEE
                self.total_volume_traded += crypto_sold * current_price
                self.balance += crypto_sold * current_price
                self.crypto_held -= crypto_sold
                self.net_worth = self.balance + self.crypto_held * \
                    current_price + self.bnb_usdt_held

            # Once again bad code from blogger
            if self.net_worth > self.max_net_worth:
                self.max_net_worth = self.net_worth

        def step(self, action, end=True):