import pandas as pd 
from finta import TA
from BB_BackTest import TradingEnv
df=pd.read_csv("../FYP_tradingBot/Sep1_March30_1h.csv")

#backTest CDC action zone 


#CDC indicator 
df['FastEMA']= TA.EMA(df,12)
df['SlowEMA']= TA.EMA(df,26)


######################################################

test_df = df[-721:]#backtest on Mrach data 

env_cdc  = TradingEnv(balance_amount=1000,balance_unit='USDT', commission=0.00075) # Binacne trading fee = 0.075%
##########################################################################################
BuyDate=[]
SellDate=[]
for i in range(len(test_df)):
    if env_cdc.balance_unit == 'USDT':
        #buy signal
        if test_df['FastEMA'].iloc[i] > test_df['SlowEMA'].iloc[i]:
            env_cdc.buy('ETH', test_df['FastEMA'].iloc[i], test_df['Date'].iloc[i])
            BuyDate.append(test_df['Date'].iloc[i])
            
                
    if env_cdc.balance_unit != 'USDT':
        if test_df['FastEMA'].iloc[i] < test_df['SlowEMA'].iloc[i]: #sell signal
            env_cdc.sell(test_df['SlowEMA'].iloc[i], test_df['Date'].iloc[i])
            SellDate.append(test_df['Date'].iloc[i])
            
#sell every ETH at the end of the month
if env_cdc.balance_unit != 'USDT':
   env_cdc.sell(test_df['Close'].iloc[-1], test_df['Date'].iloc[-1])

print('num buys: ' +str(len(env_cdc.buys)))
print('num sells: '+ str(len(env_cdc.sells)))
print('ending net worth: '+ str(env_cdc.balance_amount) + str(env_cdc.balance_unit))

k=env_cdc.buys
k.extend(env_cdc.sells)

CDC_result= pd.DataFrame(k, columns= ['Action','Unit','Amount','Price per unit','Date'])
CDC_result["Date"] = pd.to_datetime(CDC_result["Date"])
CDC_result = CDC_result.sort_values(by="Date")