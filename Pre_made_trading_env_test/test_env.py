import numpy as np
import pandas as pd

import gym
import gym_anytrading
from pandas.io.parsers import read_csv
# import quantstats as qs

from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import DQN

import matplotlib.pyplot as plt
from stable_baselines3.common.results_plotter import plot_results
import os
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy


# basic ethereum testing data
df = pd.read_csv('ETHUSD.csv', parse_dates=True, index_col='Date')
# df = gym_anytrading.datasets.STOCKS_GOOGL.copy()

df = df.dropna()

# window size Number of ticks (current and previous ticks. Candles?) returned as a Gym observation.
# It is passed in the class' constructor.
window_size = 10
start_index = window_size
end_index = len(df)


def env_maker(): return gym.make(
    'stocks-v0',
    df=df,
    window_size=window_size,
    frame_bound=(start_index, end_index)
)
from stable_baselines3.common.env_checker import check_env


# env = DummyVecEnv([env_maker])
env = DummyVecEnv([env_maker])
# check_env(env)

# # training the agent
# # policy_kwargs = dict(
# #     net_arch=[64, 'lstm', dict(vf=[128, 128, 128], pi=[64, 64])])
# model = DQN('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps=100000)

# mean_reward, std_reward = evaluate_policy(
#     model, model.get_env(), n_eval_episodes=10)
# print('=========MEAN REWARD=======')
# print(mean_reward)
# # plot_results(
# #     [log_dir], time_steps, results_plotter.X_TIMESTEPS, "DDPG LunarLander")
# # plt.show()

# env = env_maker()
# observation = env.reset()
# reward_list = []
# episode = 0
# episode_list = []
# # using trained agent
# while True:
#     observation = observation[np.newaxis, ...]

#     # action = env.action_space.sample()
#     action, _states = model.predict(observation)
#     observation, reward, done, info = env.step(action)
#     reward_list.append(reward)
#     episode += 1
#     episode_list.append(episode)
#     # env.render()
#     if done:
#         print("info:", info)
#         break

# plt.figure(figsize=(16, 6))
# env.render_all()
# plt.show()
# plt_data = {'episodes': episode_list, 'rewards': reward_list}
# print(len(episode_list))
# plt.plot(episode_list, reward_list)
# plt.show()

# # qs.extend_pandas()

# # net_worth = pd.Series(
# #     env.history['total_profit'], index=df.index[start_index+1:end_index])
# # returns = net_worth.pct_change().iloc[1:]
# # print(returns)
# # qs.reports.full(returns)
# # qs.reports.html(returns, output='a2c_quantstats.html')
