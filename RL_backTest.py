# Gym stuff
import gym
import gym_anytrading

# Stable baselines - rl stuff
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C
from stable_baselines import PPO2

from stable_baselines.common import make_vec_env

# Processing libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from gym_anytrading.envs import StocksEnv
from finta import TA

df_rl=pd.read_csv("C:/Users/i_am-/.spyder-py3/FYP_tradingBot/Jan1_March31_1h.csv")
#print(df_rl.columns.values)
cols=['OpenTime','BTC-USDT_Open',
 'BTC-USDT_High' ,'BTC-USDT_Low', 'BTC-USDT_Close' ,'BTC-USDT_volume']

df_BTC = pd.DataFrame (df_rl,columns=cols)
df_BTC['OpenTime'] =pd.to_datetime(df_BTC['OpenTime'] )

df_BTC = df_BTC.rename(columns={'BTC-USDT_Open': 'Open', 'BTC-USDT_High': 'High','BTC-USDT_Low':'Low','BTC-USDT_Close':'Close','BTC-USDT_volume':'Volume'})
df_BTC['SMA'] = TA.SMA(df_BTC, 20)
df_BTC['RSI'] = TA.RSI(df_BTC)
df_BTC.fillna(0, inplace=True)


start_date = "2022-01-01 00:00:00"
end_date="2022-03-15 23:00:00"
train_mask = (df_BTC['OpenTime'] >= start_date) & (df_BTC['OpenTime'] <= end_date)
df_BTC_train=df_BTC.loc[train_mask]

test_mask = (df_BTC['OpenTime'] >= "2022-03-16 00:00:00") & (df_BTC['OpenTime'] <= "2022-03-31 01:00:00")
df_BTC_test=df_BTC.loc[test_mask]


#24 hrs 70 days 
env_maker = lambda: gym.make('stocks-v0', df=df_BTC, frame_bound=(24,1680), window_size=24)
env = DummyVecEnv([env_maker])
#env=make_vec_env('CartPole-v1',env_maker)
model = A2C('MlpLstmPolicy', env, verbose=1) 
model.learn(total_timesteps=80000)

model.save("A2C_tocks-v0")

model = A2C.load("A2C_tocks-v0")

env = gym.make('stocks-v0', df=df_BTC, frame_bound=(1680,2137), window_size=24)
obs = env.reset()
while True: 
    obs = obs[np.newaxis, ...]
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        print("info", info)
        break
plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()

####################################################################
df_BTCM=pd.read_csv("C:/Users/i_am-/.spyder-py3/FYP_tradingBot/Download Data - CRYPTOCURRENCY_US_COINDESK_BTCUSD.csv")
df_BTCM['Date'] = pd.to_datetime(df_BTCM['Date'])
df_BTCM.sort_values('Date', ascending=True, inplace=True)
df_BTCM.set_index('Date', inplace=True)

for col in df_BTCM.columns:
    df_BTCM[col]= df_BTCM[col].str.replace(",","")

    #df_BTCM[col]=pd.to_numeric(df_BTCM[col],errors='coerce')
    df_BTCM[col] =df_BTCM['Open'].astype(float)



df_BTCM['SMA'] = TA.SMA(df_BTCM, 10)
df_BTCM['RSI'] = TA.RSI(df_BTCM)
df_BTCM.fillna(0, inplace=True)

def signals(env):
    start = env.frame_bound[0] - env.window_size
    end = env.frame_bound[1]
    prices = env.df.loc[:, 'Low'].to_numpy()[start:end]
    signal_features = env.df.loc[:, ['Low','SMA', 'RSI']].to_numpy()[start:end]
    return prices, signal_features
class MyCustomEnv(StocksEnv):
    _process_data = signals
    
env2 = MyCustomEnv(df=df_BTCM, window_size=10, frame_bound=(10,80))
env_maker = lambda: env2
env = DummyVecEnv([env_maker])
model = A2C('MlpLstmPolicy', env, verbose=1) 
model.learn(total_timesteps=30000)


env = MyCustomEnv(df=df_BTCM, window_size=10, frame_bound=(80,90))
obs = env.reset()
while True: 
    obs = obs[np.newaxis, ...]
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        print("info", info)
        break
#################################################################
#text={'Open':[46391],'High':[47367],'Low':[45174],'Close':[46304]}
text={'Open':[66391],'High':[67367],'Low':[65174],'Close':[66304]}

test = pd.DataFrame(data=text)

envt =gym.make('stocks-v0', df=test)
obst = envt.reset()

obst = obs[np.newaxis, ...]
action, _states = model.predict(obst)
obs, rewards, done, info = envt.step(action)

