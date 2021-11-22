'''Training and testing of the agents

    author: Roberto Lentini
    email: roberto.lentini@mail.utoronto.ca
    date: November 22nd 2021
'''
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from env import CryptoEnv
import pandas as pd
import os

# TODO: THIS GUY USES PRE MADE FUNCTIONS FOR THE ALGOS WHICH IS A GREAT IDEA
df = pd.read_csv('ETH-USD.csv', index_col=0)
# initiatig env
env = DummyVecEnv([lambda: CryptoEnv(df)])
# This will change for the different algorithms that will be tested
# PPO2 algo, MlpPolicy Policy object that implements actor critic, using a MLP (2 layers of 64)
model = PPO2(MlpPolicy, env, gamma=1, learning_rate=0.01, verbose=0)

# Train the agent
total_timesteps = int(os.gepytv('TOTAL_TIMESTEPS', 500000))
model.learn(total_timesteps)

# Render the graph of rewards
env.render(graph=True)

# Save the agent
# model.save('PPO2_CRYPTO')

# Trained agent performence
obs = env.reset()
env.render()
for i in range(100000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render(print_step=True)