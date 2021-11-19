'''Creating the env for the ethereum data
    Source: https://github.com/PacktPublishing/Deep-Reinforcement-Learning-Hands-On-Second-Edition/blob/master/Chapter10/lib/environ.py
    Modified: Roberto Lentini 
'''
import numpy as np
from io import DEFAULT_BUFFER_SIZE
import gym
import gym.spaces
from gym.utils import seeding
from gym.envs.registration import EnvSpec
import enum

# TODO: EDIT THE data.py TO SET UP ENV WITHT THE ADDED DATA FROM CORR ANALYSIS
import data

DEFAULT_BARS_COUNT = 10
DEFAULT_COMMISSION_PERC = 0.1


class Actions(enum.Enum):
    skip = 0
    buy = 1
    close = 2


class State:
    '''Implements most of the environments functionality.
    '''

    def __init__(self, bars_count, commission_perc,
                 reset_on_close, reward_on_close=True,
                 volumes=True):
        # checking and remembering argurments
        assert isinstance(bars_count, int)
        assert bars_count > 0
        assert isinstance(commission_perc, float)
        assert commission_perc >= 0.0
        assert isinstance(reset_on_close, bool)
        assert isinstance(reward_on_close, bool)
        self.bars_count = bars_count
        self.commission_perc = commission_perc
        self.reset_on_close = reset_on_close
        self.reward_on_close = reward_on_close
        self.volumes = volumes

    def reset(self, prices, offset):
        '''Saves the passed prices data and starting offset. Is ran everytime
            the env resets.

            we start with no position and we have no profits.

            - prices: price data
            - offset: where we left off??
        '''
        assert isinstance(prices, data.Prices)
        assert offset >= self.bars_count-1
        self.have_position = False
        self.open_price = 0.0
        self._prices = prices
        self._offset = offset

    @property
    def shape(self):
        '''Returns the shape of the state as a numpy array.21/
        '''
        # [h, l, c] * bars + position_flag + rel_profit
        if self.volumes:
            return 4 * self.bars_count + 1 + 1,
        else:
            return 3*self.bars_count + 1 + 1,

    def encode(self):
        """
            Convert current state into numpy array. 
            Formats data to be saved and visualized at the end.
        """
        res = np.ndarray(shape=self.shape, dtype=np.float32)
        shift = 0
        for bar_idx in range(-self.bars_count+1, 1):
            ofs = self._offset + bar_idx
            res[shift] = self._prices.high[ofs]
            shift += 1
            res[shift] = self._prices.low[ofs]
            shift += 1
            res[shift] = self._prices.close[ofs]
            shift += 1
            if self.volumes:
                res[shift] = self._prices.volume[ofs]
                shift += 1
        res[shift] = float(self.have_position)
        shift += 1
        if not self.have_position:
            res[shift] = 0.0
        else:
            res[shift] = self._cur_close() / self.open_price - 1.0
        return res

    def _cur_close(self):
        """
            Calculate real close price for the current bar
        """
        open = self._prices.open[self._offset]
        rel_close = self._prices.close[self._offset]
        return open * (1.0 + rel_close)

    def step(self, action):
        """
        Perform one step in our price, adjust offset, check for the end of prices
        and handle position change
        :param action:
        :return: reward, done
        """
        assert isinstance(action, Actions)
        reward = 0.0
        done = False
        close = self._cur_close()
        # if we do not have a position and we want to buy
        if action == Actions.Buy and not self.have_position:
            self.have_position = True
            self.open_price = close
            reward -= self.commission_perc
        # if we have position and want to close
        elif action == Actions.Close and self.have_position:
            reward -= self.commission_perc
            done |= self.reset_on_close
            if self.reward_on_close:
                reward += 100.0 * (close / self.open_price - 1.0)
            self.have_position = False
            self.open_price = 0.0
        # resent the offset (start point) and give the reward for the last candle
        self._offset += 1
        prev_close = close
        close = self._cur_close()
        done |= self._offset >= self._prices.close.shape[0]-1

        if self.have_position and not self.reward_on_close:
            reward += 100.0 * (close / prev_close - 1.0)

        return reward, done


class State1D(State):
    """
    State with shape suitable for 1D convolution
    """
    @property
    def shape(self):
        if self.volumes:
            return (6, self.bars_count)
        else:
            return (5, self.bars_count)

    def encode(self):
        res = np.zeros(shape=self.shape, dtype=np.float32)
        start = self._offset-(self.bars_count-1)
        stop = self._offset+1
        res[0] = self._prices.high[start:stop]
        res[1] = self._prices.low[start:stop]
        res[2] = self._prices.close[start:stop]
        if self.volumes:
            res[3] = self._prices.volume[start:stop]
            dst = 4
        else:
            dst = 3
        if self.have_position:
            res[dst] = 1.0
            res[dst+1] = self._cur_close() / self.open_price - 1.0
        return res


class CryptoEnv(gym.Env):
    '''Setting up the crypto enviroment

        - prices: dict of one or more crypto prices
        - bars_count: int of number of candles that are passed in the observation
        - comission: int of the percent we pay on broker fee for buying and selling
        - reset_on_close: bool, if TRUE the episode will stop when the agent closes it's positon
            if this if FALSE it will continue until the end of the time series
        - conv_1d: bool, if FALSE we have data in a vector format ie [[high, low, close], [high, low, close], ...],
            if TRUE we have long data in a matrix format [[all highs], [all lows], [all close]]. Allows us
            to switch between different data representations for our neural network
        - random_start_on_reset: if TRUE, when the environment resets a random point in the time series will be selected.
            if FALSE it will start from the beginning of the data.
        - reward_on_close: if TRUE, the agent will receive a reward on close. If FALSE the agent will receive
            a small reward at each candle.
        - volumes: switches on volumes in observations (TODO REMOVE THIS IF IT DOES WHAT I THINK IT DOES)
    '''
    metadata = {'render.modes': ['humans']}
    spec = EnvSpec("CryptoEnv-v0")

    def __init__(self, prices, bars_count=DEFAULT_BARS_COUNT,
                 commission=DEFAULT_COMMISSION_PERC,
                 reset_on_close=True, state_1d=False,
                 random_ofs_on_reset=True, reward_on_close=False,
                 volumes=False):

        assert isinstance(prices, dict)

        self._prices = prices
        if state_1d:
            self._state = State1D(bars_count, commission, reset_on_close, reward_on_close,
                                  volumes=volumes)
        else:
            self._state = State(
                bars_count, commission, reset_on_close,
                reward_on_close=reward_on_close, volumes=volumes)
        self.action_space = gym.spaces.Discrete(n=len(Actions))
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf,
            shape=self._state.shape, dtype=np.float32)
        self.random_ofs_on_reset = random_ofs_on_reset
        self.seed()

        def reset(self):
            '''Dictates how the environment will be reset.
            '''
            # make selection of the instrument and it's offset. Then reset the state
            self._instrument = self.np_random.choice(
                list(self._prices.keys()))
            prices = self._prices[self._instrument]
            bars = self._state.bars_count
            if self.random_ofs_on_reset:
                offset = self.np_random.choice(
                    prices.high.shape[0]-bars*10) + bars
            else:
                offset = bars
            self._state.reset(prices, offset)
            return self._state.encode()

        def step(self, action_idx):
            '''Dictates how steps are taking in the environment.

                - action_idx: the index of the action to take.
            '''
            action = Actions(action_idx)
            reward, done = self._state.step(action)
            obs = self._state.encode()
            info = {
                "instrument": self._instrument,
                "offset": self._state._offset
            }
            return obs, reward, done, info

        def render(self, mode='human', close=False):
            '''Can render the current state in human or machine readable format.
                Currently not being used in our env.
            '''
            pass

        def close(self):
            '''Gets called on the enviroment destruction to free resources.
            '''
            pass

        def seed(self, seed=None):
            '''Allows to generate multiple random environments at once. This is useful
                for algorithms using multiple environments at once such as A3C.
            '''
            self.np_random, seed1 = seeding.np_random(seed)
            seed2 = seeding.hash_seed(seed1 + 1) % 2 ** 31

            return [seed1, seed2]

        # TODO: MODIFY THIS FOR MY USE CASE

        @classmethod
        def from_dir(cls, data_dir, **kwargs):
            '''Load data into the enviroment (only has 5 columns)
            '''
            prices = {
                file: data.load_relative(file)
                for file in data.price_files(data_dir)
            }
