'''This is a custom cryptocurrency trading environment created with
    openAi gym.

    modified from: https://github.com/pythonlessons/RL-Bitcoin-trading-bot/tree/main/RL-Bitcoin-trading-bot_1
    author: Roberto Lentini
    email: roberto.lentini@mail.utoronto.ca
    date: November 23rd 2021
'''
from numpy.core.fromnumeric import shape
from stable_baselines3.common.env_checker import check_env
import pandas as pd
from collections import deque
import random
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import DQN


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df, initial_balance=1000, lookback_window_size=50, trading_fee=0.1):
        '''Initiating the parameters.

            - df: pandas dataframe with historical crypto data.
            - initial_balance: int of the starting balance to trade.
            - lookback_window_size: int of number of candles we want
                our agent to see. (the candle period, ie daily, hourly... depends on the data given)
            - trading_fee: the percent of fee payed on every order.
        '''
        super(CustomEnv, self).__init__()
        # Define action and observation space
        self.df = df
        self.trading_fee = trading_fee
        self.df_total_steps = len(self.df) - 1
        self.initial_balance = initial_balance
        self.lookback_window_size = lookback_window_size

        # Orders history contains the balance, net_worth, crypto_bought, crypto_sold, crypto_held values for the last lookback_window_size steps
        self.orders_history = deque(maxlen=self.lookback_window_size)

        # Market history contains the open, high, low, close, volume values for the last lookback_window_size prices
        # self.market_history = deque(maxlen=self.lookback_window_size)
        self.market_history = {'Open' : deque(maxlen=self.lookback_window_size),
        'High' : deque(maxlen=self.lookback_window_size),
        'Low' : deque(maxlen=self.lookback_window_size),
        'Close' : deque(maxlen=self.lookback_window_size),
        'Volume' : deque(maxlen=self.lookback_window_size),
        }
        # State size contains Market+Orders history for the last lookback_window_size steps
        # TODO: the 10 will be switch the the number of columns in the crypto_analysis dataset
        self.state_size = (self.lookback_window_size, 10)
        # spaces
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=self.state_size, dtype=np.float32)
        dict = {
            'Open': gym.spaces.Box(low=-np.inf, high=np.inf, shape=(10,)),
            'High': gym.spaces.Box(low=-np.inf, high=np.inf, shape=(10,)),
            'Low': gym.spaces.Box(low=-np.inf, high=np.inf, shape=(10,)),
            'Close': gym.spaces.Box(low=-np.inf, high=np.inf, shape=(10,)),
            'Volume': gym.spaces.Box(low=-np.inf, high=np.inf, shape=(10,)),
            } 
        self.observation_space = gym.spaces.Dict(dict)
        # actions ([hold, buy, sell])
        self.action_space = spaces.Discrete(3)

    def _next_observation(self):
        '''Get the data points for the given current_step
        '''
        # TODO: modify this for my enviromental variables
        # self.market_history.append([self.df.loc[self.current_step, 'Open'],
        #                             self.df.loc[self.current_step, 'High'],
        #                             self.df.loc[self.current_step, 'Low'],
        #                             self.df.loc[self.current_step, 'Close'],
        #                             self.df.loc[self.current_step, 'Volume']
        #                             ])
        # TODO: this method of going from np.array to  deque to append and then back to 
        #       numpy.array to please openAi gym is sketchy
        
        if isinstance(self.market_history["Open"],np.ndarray):
            self.market_history = {'Open': deque(self.market_history["Open"].tolist(), maxlen=self.lookback_window_size),
                                        'High' : deque(self.market_history["High"].tolist(), maxlen=self.lookback_window_size),
                                        'Low' : deque(self.market_history["Low"].tolist(), maxlen=self.lookback_window_size),
                                        'Close' : deque(self.market_history["Close"].tolist(), maxlen=self.lookback_window_size),
                                        'Volume' : deque(self.market_history["Volume"].tolist(), maxlen=self.lookback_window_size)}

        self.market_history["Open"].append(self.df.loc[self.current_step, 'Open'])
        self.market_history["High"].append(self.df.loc[self.current_step, 'High'])
        self.market_history["Low"].append(self.df.loc[self.current_step, 'Low'])
        self.market_history["Close"].append(self.df.loc[self.current_step, 'Close'])
        self.market_history["Volume"].append(self.df.loc[self.current_step, 'Volume'])

        self.market_history = {'Open': np.array(self.market_history["Open"]),
                                    'High' : np.array(self.market_history["High"]),
                                    'Low' : np.array(self.market_history["Low"]),
                                    'Close' : np.array(self.market_history["Close"]),
                                    'Volume' : np.array(self.market_history["Volume"])
        }   

        obs = self.market_history
        # obs = np.concatenate(
        #     (self.market_history, self.orders_history), axis=1)
        return obs

    def step(self, action):
        '''Execute a step in the env.

            - action: int of the action to take
        '''
        self.crypto_bought = 0
        self.crypto_sold = 0
        self.current_step += 1

        # Set the current price to close
        current_price = self.df.loc[self.current_step, 'Close']
        # Hold
        if action == 0:
            pass

        # Buy with 100% of current balance TODO: confirm the math for crypto bought
        elif action == 1 and self.balance > 0:
            self.crypto_bought = (
                self.balance - (self.trading_fee * self.balance)) / current_price
            self.balance -= self.crypto_bought * current_price
            self.crypto_held += self.crypto_bought

        # Sell 100% of current crypto held TODO: confirm the math for balance
        elif action == 2 and self.crypto_held > 0:
            self.crypto_sold = self.crypto_held
            self.balance += (self.crypto_sold * current_price) - \
                ((self.crypto_sold * current_price) * self.trading_fee)
            self.crypto_held -= self.crypto_sold

        self.prev_net_worth = self.net_worth
        self.net_worth = self.balance + self.crypto_held * current_price

        # keeping track of transactions TODO: add time point for visualization
        self.orders_history.append(
            [self.balance, self.net_worth, self.crypto_bought, self.crypto_sold, self.crypto_held])
        
        # Calculate reward is the diff between total trading profits in percent - total eth gains in percent
        # TODO: maked sure the reward functions is doing the proper calculations
        buy_and_hold_gains_percent = (
            self.df.loc[self.current_step, 'Close'] / self.df.loc[0, 'Close']) * 100
        profit_percent = ((self.net_worth - self.initial_balance) /
                          self.initial_balance) * 100
        reward = profit_percent - buy_and_hold_gains_percent

        # if the agent halves the starting balance it has lost the game
        if self.net_worth <= self.initial_balance/2:
            done = True
        else:
            done = False

        obs = self._next_observation()
        # required
        info = dict(
            total_reward = reward,
            total_profit = self.net_worth - self.initial_balance,
        )
        return obs, reward, done, info

    def reset(self, env_steps_size=0):
        '''Reset the env to an initial state.

            - env_step_size: int changes the step size for training the data.
                An alternative to random initial offset.
        '''
        self.balance = self.initial_balance
        self.net_worth = self.initial_balance
        self.prev_net_worth = self.initial_balance
        self.crypto_held = 0
        self.crypto_sold = 0
        self.crypto_bought = 0

        # TODO: use more elegant method
        # converting the np.arrays to list for function to work
        if isinstance(self.market_history["Open"],np.ndarray):
            self.market_history = {'Open': deque(self.market_history["Open"].tolist(), maxlen=self.lookback_window_size),
                                        'High' : deque(self.market_history["High"].tolist(), maxlen=self.lookback_window_size),
                                        'Low' : deque(self.market_history["Low"].tolist(), maxlen=self.lookback_window_size),
                                        'Close' : deque(self.market_history["Close"].tolist(), maxlen=self.lookback_window_size),
                                        'Volume' : deque(self.market_history["Volume"].tolist(), maxlen=self.lookback_window_size)}
        if env_steps_size > 0:  # used for training dataset
            self.start_step = random.randint(
                self.lookback_window_size, self.df_total_steps - env_steps_size)
            self.end_step = self.start_step + env_steps_size
        else:  # used for testing dataset
            self.start_step = self.lookback_window_size
            self.end_step = self.df_total_steps

        self.current_step = self.start_step

        for i in reversed(range(self.lookback_window_size)):
            current_step = self.current_step - i
            self.orders_history.append(
                [self.balance, self.net_worth, self.crypto_bought, self.crypto_sold, self.crypto_held])
            # self.market_history.append([self.df.loc[current_step, 'Open'],
            #                             self.df.loc[current_step, 'High'],
            #                             self.df.loc[current_step, 'Low'],
            #                             self.df.loc[current_step, 'Close'],
            #                             self.df.loc[current_step, 'Volume']
            #                             ])
            self.market_history["Open"].append(self.df.loc[current_step, 'Open'])
            self.market_history["High"].append(self.df.loc[current_step, 'High'])
            self.market_history["Low"].append(self.df.loc[current_step, 'Low'])
            self.market_history["Close"].append(self.df.loc[current_step, 'Close'])
            self.market_history["Volume"].append(self.df.loc[current_step, 'Volume'])

        self.market_history = {'Open': np.array(self.market_history["Open"]),
                                    'High' : np.array(self.market_history["High"]),
                                    'Low' : np.array(self.market_history["Low"]),
                                    'Close' : np.array(self.market_history["Close"]),
                                    'Volume' : np.array(self.market_history["Volume"])
        }        
        # state = np.concatenate(
        #     (self.market_history, self.orders_history), axis=1)
        state = self.market_history
        print('==============HERE===================')
        print(state)
        return state  # reward, done, info can't be included

    def render(self, mode='human'):
        '''Allows us to visualize how the agent learns.
        '''
        print(f'Step: {self.current_step}, Net Worth: {self.net_worth}')
        


#  ================= END OF ENV SETUP =============================

def Random_games(env, train_episodes=50, training_batch_size=500):
    '''Makes the agent trade randomly. This can be used as a baseline.

        - train_episodes: int for the amount of episodes to train agent.
        - training_batch_size: int of the number of steps per episode
    '''
    average_net_worth = 0
    for episode in range(train_episodes):
        state = env.reset(env_steps_size=training_batch_size)

        while True:
            env.render()

            action = np.random.randint(3, size=1)[0]

            state, reward, done, info = env.step(action)

            if env.current_step == env.end_step:
                average_net_worth += env.net_worth
                print("net_worth:", env.net_worth)
                break

    print("average_net_worth:", average_net_worth/train_episodes)


df = pd.read_csv('ETHUSD.csv')

lookback_window_size = 10
train_df = df[:-720-lookback_window_size]
test_df = df[-720-lookback_window_size:]  # 30 days

train_env = CustomEnv(train_df, lookback_window_size=lookback_window_size)
test_env = CustomEnv(test_df, lookback_window_size=lookback_window_size)
env = CustomEnv(df, lookback_window_size=lookback_window_size)
# check_env(env)

Random_games(train_env, train_episodes=10, training_batch_size=500)
# model = DQN("MultiInputPolicy", env, verbose=1)
# model.learn(total_timesteps=10000, log_interval=4)

# obs = env.reset()
# while True:
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#       obs = env.reset()