import requests
import pandas as pd
from datetime import datetime, timezone, timedelta

markets_details_api = "https://api.coindcx.com/exchange/v1/markets_details"
response = requests.get(markets_details_api)
data = response.json()
df=pd.DataFrame(data)
usdt_pairs_df=df[(df.base_currency_short_name=='USDT') & (df.max_leverage>0) & (df.status=='active') ] 
usdt_pairs_df.rename(columns={'symbol':'market'}, inplace=True)
usdt_pairs_df=usdt_pairs_df[['target_currency_short_name','market']]

def get_latest_api_data(usdt_pairs_df):
    print('ticker api is calling...')
    final_df=None
    stream_api='https://api.coindcx.com/exchange/ticker'
    response = requests.get(stream_api)
    if response.status_code==200:
        stream_data = response.json()
    else:
        raise('')
    stream_df=pd.json_normalize(stream_data)
    # stream_df.rename(columns={'market':'symbol'}, inplace=True)

    final_df=pd.merge(usdt_pairs_df,stream_df,on='market',how='inner')
    ist_offset = timedelta(hours=5, minutes=30)
    final_df['ist_time'] = pd.to_datetime(final_df['timestamp'], unit='s', utc=True) + ist_offset
    return final_df