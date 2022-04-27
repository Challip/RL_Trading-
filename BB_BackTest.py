import pandas as pd 
from finta import TA
from ta.volatility import BollingerBands
df=pd.read_csv("C:/Users/i_am-/.spyder-py3/FYP_tradingBot/Sep1_March30_1h.csv")
test_df = df[-721:]# test on March data 
ww= test_df.loc[:, 'Close']
#bollinger band indicator 
indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)
df['bb_bbm'] = indicator_bb.bollinger_mavg()
df['bb_bbh'] = indicator_bb.bollinger_hband()
df['bb_bbl'] = indicator_bb.bollinger_lband()


test_df = df[-721:]#backtest on Mrach data 
##########################################################

###############################################################################

#trading environment to keep track of data

class TradingEnv:
    def __init__(self, balance_amount, balance_unit, commission):
        self.balance_amount = balance_amount
        self.balance_unit = balance_unit
        self.commission=commission
        self.crypto_held=0
        self.buys = []
        self.sells = []
    def buy(self, buy_unit, buy_price, time):
        buy_amount= (self.balance_amount / buy_price) 
        cost=buy_amount*buy_price*(1 + self.commission)
        self.balance_amount -= cost
        self.crypto_held += buy_amount
        self.balance_unit = buy_unit
        # buy history
        self.buys.append(["BUY",buy_unit,buy_amount,buy_price,time])
        
    def sell(self, sell_price, time):
        sell_amount= self.crypto_held
        sell_cost= sell_amount * sell_price  * (1 - self.commission)
        self.balance_amount += sell_cost
        self.crypto_held -=sell_amount
        self.balance_unit = 'USDT'
        
        self.sells.append( ["SELL",self.balance_unit,sell_amount, sell_price,time] )
        

env  = TradingEnv(balance_amount=1000,balance_unit='USDT', commission=0.00075) # Binacne trading fee = 0.075%
##########################################################################################
for i in range(len(test_df)):
    if env.balance_unit == 'USDT':
        if test_df['Close'].iloc[i] < test_df['bb_bbl'].iloc[i]: #buy at bb_bbl
            env.buy('ETH', test_df['bb_bbl'].iloc[i], test_df['Date'].iloc[i])
                
    if env.balance_unit != 'USDT':
        if test_df['Open'].iloc[i] > test_df['bb_bbh'].iloc[i]: #sell at bb_bbh
            env.sell(test_df['bb_bbh'].iloc[i], test_df['Date'].iloc[i])
            
            
#sell every ETH at the end of the month
if env.balance_unit != 'USDT':
   env.sell(test_df['Close'].iloc[-1], test_df['Date'].iloc[-1])



print('num buys: ' +str(len(env.buys)))
print('num sells: '+ str(len(env.sells)))
print('ending net worth: '+ str(env.balance_amount) + str(env.balance_unit))

F=env.buys
F.extend(env.sells)
BB_result= pd.DataFrame(F, columns= ['Action','Unit','Amount','Price per unit','Date'])

BB_result["Date"] = pd.to_datetime(BB_result["Date"])
BB_result = BB_result.sort_values(by="Date")

