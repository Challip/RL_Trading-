
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import copy
import pandas as pd
import numpy as np
import random
from collections import deque
from tensorboardX import SummaryWriter
from tensorflow.keras.optimizers import Adam, RMSprop
from model import Actor_Model, Critic_Model, Shared_Model
from draw import TradingGraph, Write_to_file
import matplotlib.pyplot as plt
from datetime import datetime
from indicators import AddIndicators

def cdc_reset(self, env_steps_size = 0):
     self.visualization = TradingGraph(Render_range=self.Render_range, Show_reward=self.Show_reward) # init visualization
     self.trades = deque(maxlen=self.Render_range) # limited orders memory for visualization
     
     self.balance = self.initial_balance
     self.net_worth = self.initial_balance
     self.prev_net_worth = self.initial_balance
     self.crypto_held = 0
     self.crypto_sold = 0
     self.crypto_bought = 0
     self.episode_orders = 0 # track episode orders count
     self.prev_episode_orders = 0 # track previous episode orders count
     self.rewards = deque(maxlen=self.Render_range)
     self.env_steps_size = env_steps_size
     self.punish_value = 0
     if env_steps_size > 0: # used for training dataset
         self.start_step = random.randint(self.lookback_window_size, self.df_total_steps - env_steps_size)
         self.end_step = self.start_step + env_steps_size
     else: # used for testing dataset
         self.start_step = self.lookback_window_size
         self.end_step = self.df_total_steps
         
     self.current_step = self.start_step
    
     for i in reversed(range(self.lookback_window_size)):
         current_step = self.current_step - i
         self.orders_history.append([self.balance, self.net_worth, self.crypto_bought, self.crypto_sold, self.crypto_held])
    
         self.market_history.append([self.df.loc[current_step, 'Open'],
                                     self.df.loc[current_step, 'High'],
                                     self.df.loc[current_step, 'Low'],
                                     self.df.loc[current_step, 'Close'],
                                     self.df.loc[current_step, 'Volume'],
                                     ])
    
         self.indicators_history.append(
                                     [
                                     self.df.loc[current_step, 'ema_12'] / self.normalize_value,
                                     self.df.loc[current_step, 'ema_26'] / self.normalize_value,

                                     ])
         
    
     state = np.concatenate((self.market_history, self.orders_history), axis=1) / self.normalize_value
     state = np.concatenate((state, self.indicators_history), axis=1)
    
     return state

 # Get the data points for the given current_step
def _cdc_next_observation(self):
    self.market_history.append([self.df.loc[self.current_step, 'Open'],
                                self.df.loc[self.current_step, 'High'],
                                self.df.loc[self.current_step, 'Low'],
                                self.df.loc[self.current_step, 'Close'],
                                self.df.loc[self.current_step, 'Volume'],
                                ])

    self.indicators_history.append([self.df.loc[self.current_step, 'ema_12'] / self.normalize_value,
                                self.df.loc[self.current_step, 'ema_26'] / self.normalize_value,

                                ])

    obs = np.concatenate((self.market_history, self.orders_history), axis=1) / self.normalize_value
    obs = np.concatenate((obs, self.indicators_history), axis=1)
    
    return obs