import pandas as pd
from binance.client import Client
from APIkey import api_key,secret_key
import time
from datetime import datetime


client = Client(api_key, secret_key)


coins =['ETH','LTC','OMG','BTC']
#coins =['ETH']
merge=False
for coin in coins:
    
    start_str='September 1, 2021'
    end_str="March 31, 2022"
    #coin price every 1 hr 
    ohlcv=client.get_historical_klines(symbol=f'{coin}USDT', interval=client.KLINE_INTERVAL_1HOUR, start_str=start_str,end_str=end_str )
    cols = ['OpenTime',
            f'{coin}-USDT_Open',
            f'{coin}-USDT_High',
            f'{coin}-USDT_Low',
            f'{coin}-USDT_Close',
            f'{coin}-USDT_volume',
            'CloseTime',
            f'{coin}-QuoteAssetVolume',
            f'{coin}-NumberOfTrades',
            f'{coin}-TBBAV',
            f'{coin}-TBQAV',
            f'{coin}-ignore']
    coin_df=pd.DataFrame(ohlcv,columns=cols)
    
    if merge == True:
        all_coins_df = pd.merge(coin_df,all_coins_df,how='inner',on=['OpenTime','CloseTime'])
    else:
        all_coins_df= coin_df
        merge=True
        
    time.sleep(60)
#change formate of opening and closing time 
all_coins_df['OpenTime'] = [datetime.fromtimestamp(ts / 1000) for ts in all_coins_df['OpenTime']]
all_coins_df['CloseTime'] = [datetime.fromtimestamp(ts / 1000) for ts in all_coins_df['CloseTime']]     

#convert price to float except time columns 
for col in all_coins_df.columns:
    if not 'Time' in col:
        all_coins_df[col] = all_coins_df[col].astype(float)

print ("Finish collecting data")        
##################################################################################        

cols=['OpenTime','ETH-USDT_Open','ETH-USDT_High' ,'ETH-USDT_Low', 'ETH-USDT_Close' ,'ETH-USDT_volume']
df_f = pd.DataFrame (all_coins_df,columns=cols)
df_f = df_f.rename(columns={'OpenTime':'Date','ETH-USDT_Open': 'Open', 'ETH-USDT_High': 'High','ETH-USDT_Low':'Low','ETH-USDT_Close':'Close','ETH-USDT_volume':'Volume'})
df_f.to_csv('Sep1_March30_1h.csv',index=False)

