import ta
import pandas as pd
from BB_BackTest import TradingEnv


df=pd.read_csv("../FYP_tradingBot/Sep1_March30_1h.csv")

#stochastic oscillator indicators
df['%K'] = ta.momentum.stoch(df.High, df.Low, df.Close, window=14, smooth_window=3)
df['%D'] = df['%K'].rolling(3).mean()

#Rrelative strength index 
df['RSI'] = ta.momentum.rsi(df.Close, window=14)

#Moving average convergence divergence 
short=df['Close'].ewm(span=12, adjust=False).mean()
long=df['Close'].ewm(span=26, adjust=False).mean()
macd = short-long
signalM = macd.ewm(span=9, adjust=False).mean()

df['MACD']= macd
df['signalM']=signalM


test_df = df[-721:]#backtest on Mrach data 
env_msr  = TradingEnv(balance_amount=1000,balance_unit='USDT', commission=0.00075) # Binacne trading fee = 0.075%

BuyDate=[]
SellDate=[]
for i in range(len(test_df)):
    if env_msr.balance_unit == 'USDT':
        #buy signal
        if (test_df['%K'].iloc[i] <= 30) & (test_df['%D'].iloc[i] <= 30) & (test_df['MACD'].iloc[i] > test_df['signalM'].iloc[i]):
           env_msr.buy('ETH', test_df['Close'].iloc[i], test_df['Date'].iloc[i])#buy at the close price of that hour 
           BuyDate.append(test_df['Date'].iloc[i])
                
    if env_msr.balance_unit != 'USDT':
        if (test_df['%K'].iloc[i] <= 70) & (test_df['%D'].iloc[i] <= 70) & (test_df['MACD'].iloc[i] < test_df['signalM'].iloc[i]):
            env_msr.sell( test_df['Close'].iloc[i] , test_df['Date'].iloc[i])#sell at the close price of that hour
            SellDate.append(test_df['Date'].iloc[i])

#sell every ETH at the end of the month
if env_msr.balance_unit != 'USDT':
   env_msr.sell(test_df['Close'].iloc[-1], test_df['Date'].iloc[-1])
   
print('num buys: ' +str(len(env_msr.buys)))
print('num sells: '+ str(len(env_msr.sells)))
print('ending net worth: '+ str(env_msr.balance_amount) + str(env_msr.balance_unit))


S=env_msr.buys
S.extend(env_msr.sells)

MSR_result= pd.DataFrame(S, columns= ['Action','Unit','Amount','Price per unit','Date'])
MSR_result["Date"] = pd.to_datetime(MSR_result["Date"])
MSR_result = MSR_result.sort_values(by="Date")