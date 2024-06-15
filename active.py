from flask import Flask, render_template ,request,jsonify
from forex_python.converter import CurrencyRates
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine 
import pymysql
pymysql.install_as_MySQLdb()
from threading import Thread
from datetime import datetime, timezone, timedelta
from stream_dataframe_script import get_latest_api_data
import hmac
import hashlib
import base64
import json
import time
import requests
import pandas as pd
import datetime
import cred

app = Flask(__name__)

# Your API Key and Secret
# account1
# fathers account
key1=cred.key1
secret1 = cred.secret1
# account2 shekhar2
key2=cred.key2
secret2 = cred.secret2

# account3 chaitanya3
key3 = cred.key3
secret3 = cred.secret3

# account4 chaitanya4
key4 = cred.key4
secret4 = cred.secret4

# account5 anita5
key5 = cred.key5
secret5 = cred.key5

# key6='9a6'
# secret6='9a6'


allAcounts= ["account1","account2","account3","account4","account5"]
roundOfMap = {'BTTCUSDT':0,'DOGEUSDT':0,'MATICUSDT':0,'XRPUSDT':0,'CFXUSDT':0,'CHZUSDT':0,'FTMUSDT':0,'HBARUSDT':0,'LINKUSDT':2,'SHIBUSDT':0,'XLMUSDT':0,'ZRTUSDT':0,'ALGOUSDT':0,'GALAUSDT':0,'MANAUSDT':0,'SANDUSDT':0,'GRTUSDT':0,
'CKBUSDT':0,'ALPHAUSDT':0,'COTIUSDT':0,'LRCUSDT':0,'TRUUSDT':0,'BATUSDT':0,'BLZUSDT':0,'CTSIUSDT':0,'DENTUSDT':0,'DUSKUSDT':0,'FLMUSDT':0,'HARDUSDT':0,'IOSTUSDT':0,'NKNUSDT':0,'OCEANUSDT':0,'ONTUSDT':0,
'XEMUSDT':0,'ZRXUSDT':0,'AKROUSDT':0,'AMPUSDT':0,'BETAUSDT':0,'CHRUSDT':0,'CTXCUSDT':0,'DARUSDT':0,'DOCKUSDT':0,'FISUSDT':0,'FUNUSDT':0,'HIVEUSDT':0,'HOTUSDT':0,'IOTAUSDT':0,'IOTXUSDT':0,'MBLUSDT':0,
'NULSUSDT':0,'OGNUSDT':0,'OMUSDT':0,'ONGUSDT':0,'OOKIUSDT':0,'PNTUSDT':0,'REEFUSDT':0,'RENUSDT':0,'REQUSDT':0,'SCUSDT':0,'SKLUSDT':0,'SLPUSDT':0,'SPELLUSDT':0,'STMXUSDT':0,'STORJUSDT':0,'SUPERUSDT':0,
'SYSUSDT':0,'TFUELUSDT':0,'TLMUSDT':0,'TROYUSDT':0,'TWTUSDT':0,'UTKUSDT':0,'WANUSDT':0,'WAXPUSDT':0,
'ADAUSDT':1,'1INCHUSDT':1,'CRVUSDT':1,'RUNEUSDT':1,'EOSUSDT':1,'TRXUSDT':1,'MINAUSDT':1,'NEARUSDT':1,'SUSHIUSDT':1,'MASKUSDT':1,'ASTRUSDT':1,'KNCUSDT':1,'MTLUSDT':1,'RUNEUSDT':1,'THETAUSDT':1,'VETUSDT':1,
'CELOUSDT':1,'ICXUSDT':1,'INJUSDT':1,'KAVAUSDT':1,'SNXUSDT':1,'STXUSDT':1,'XTZUSDT':1,'ZILUSDT':1,'ANKRUSDT':1,'ARPAUSDT':1,'AUDIOUSDT':1,'BANDUSDT':1,'KLAYUSDT':1,'LITUSDT':1,'ONEUSDT':1,'PEOPLEUSDT':1,
'RADUSDT':1,'ALPACAUSDT':1,'ANTUSDT':1,'BELUSDT':1,'BNTUSDT':1,'BSWUSDT':1,'CELRUSDT':1,'COSUSDT':1,'DATAUSDT':1,'DGBUSDT':1,'DODOUSDT':1,'ENJUSDT':1,'FIROUSDT':1,'GHSTUSDT':1,'GLMRUSDT':1,'JSTUSDT':1,
'LSKUSDT':1,'POLSUSDT':1,'PUNDIXUSDT':1,'QTUMUSDT':1,'RLCUSDT':1,'ROSEUSDT':1,'RVNUSDT':1,'STPTUSDT':1,'STRAXUSDT':1,'SUNUSDT':0,'SXPUSDT':1,'TKOUSDT':1,'UMAUSDT':1,'UNFIUSDT':1,'WRXUSDT':1,'YGGUSDT':1,
'AVAXUSDT':2,'AXSUSDT':2,'ETCUSDT':2,'SOLUSDT':2,'FILUSDT':2,'ATOMUSDT':2,'APEUSDT':2,'DYDXUSDT':2,'FLOWUSDT':2,'RNDRUSDT':2,'NEOUSDT':2,'WAVESUSDT':2,'IMXUSDT':2,'UNIUSDT':2,'EGLDUSDT':2,'ICPUSDT':2,
'LPTUSDT':2,'ZENUSDT':2,'CAKEUSDT':2,'XVSUSDT':2,'ALICEUSDT':2,'API3USDT':2,'BALUSDT':2,'BICOUSDT':2,'CITYUSDT':2,'DEGOUSDT':2,'FLUXUSDT':2,'JOEUSDT':2,'KDAUSDT':2,'KP3RUSDT':2,'LUNAUSDT':2,
'NMRUSDT':2,'PERPUSDT':2,'PONDUSDT':2,'PSGUSDT':2,'TRBUSDT':2,'WINGUSDT':2,'WNXMUSDT':2,'XNOUSDT':2,
'MOVRUSDT':3,'KSMUSDT':3,'AAVEUSDT':3,'BNBUSDT':3,'BCHUSDT':3,'LTCUSDT':3,'XMRUSDT':3,'ZECUSDT':3,'QNTUSDT':3,'DASHUSDT':3,'COMPUSDT':3,'CVXUSDT':3,'ILVUSDT':3,'KSMUSDT':3,'PYRUSDT':3,
'ETHUSDT':4,'MKRUSDT':4,
'BTCUSDT':5,'YFIUSDT':5
}


@app.route('/account1')
def index():
    key = key1
    secret = secret1
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    timeStamp = int(round(time.time() * 1000))
    balanceData = fetch_balance(key,secret)

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    print(signature)

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
 
    ticker_data = fetch_line_graph_data()
    merged_map = []

    for item1 in data:
      for item2 in ticker_data:
        if item1.get('market') == item2.get('market'):
           merged_item = {**item1, **item2}
           merged_map.append(merged_item)

    
    return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
@app.route('/account2')
def anotherIndex():
    key = key2
    secret = secret2
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    balanceData = fetch_balance(key,secret)
    timeStamp = int(round(time.time() * 1000))

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    print(signature)

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
 
    ticker_data = fetch_line_graph_data()
    merged_map = []

    for item1 in data:
      for item2 in ticker_data:
        if item1.get('market') == item2.get('market'):
            merged_item = {**item1, **item2}
            merged_map.append(merged_item)

    return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
    
     
@app.route('/account3')
def account3Index():
    key = key3
    secret = secret3
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    balanceData = fetch_balance(key,secret)
    timeStamp = int(round(time.time() * 1000))

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    print(signature)

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
 
    ticker_data = fetch_line_graph_data()
    merged_map = []

    for item1 in data:
      for item2 in ticker_data:
        if item1.get('market') == item2.get('market'):
            merged_item = {**item1, **item2}
            merged_map.append(merged_item)

    
    return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
@app.route('/account4')
def account4Index():
    key = key4
    secret = secret4
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    balanceData = fetch_balance(key,secret)
    timeStamp = int(round(time.time() * 1000))

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    print(signature)

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
 
    ticker_data = fetch_line_graph_data()
    merged_map = []

    for item1 in data:
      for item2 in ticker_data:
        if item1.get('market') == item2.get('market'):
            merged_item = {**item1, **item2}
            merged_map.append(merged_item)

    
    return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
@app.route('/account5')
def account5Index():
    key = key5
    secret = secret5
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    balanceData = fetch_balance(key,secret)
    timeStamp = int(round(time.time() * 1000))

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    print(signature)

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
 
    ticker_data = fetch_line_graph_data()
    merged_map = []

    for item1 in data:
      for item2 in ticker_data:
        if item1.get('market') == item2.get('market'):
            merged_item = {**item1, **item2}
            merged_map.append(merged_item)

    
    return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
# @app.route('/account6')
# def account6Index():
#     key = key6
#     secret = secret6
#     # Your API request logic here
#     secret_bytes = bytes(secret, encoding='utf-8')
#     balanceData = fetch_balance(key,secret)
#     timeStamp = int(round(time.time() * 1000))

#     body = {
#         "details": True,
#         "status": "open",
#         "size": 200,
#         "timestamp": timeStamp
#     }

#     json_body = json.dumps(body, separators=(',', ':'))

#     signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
#     print(signature)

#     url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

#     headers = {
#         'Content-Type': 'application/json',
#         'X-AUTH-APIKEY': key,
#         'X-AUTH-SIGNATURE': signature
#     }

#     response = requests.post(url, data=json_body, headers=headers)
#     data = response.json()
 
#     ticker_data = fetch_line_graph_data()
#     merged_map = []

#     for item1 in data:
#       for item2 in ticker_data:
#         if item1.get('market') == item2.get('market'):
#             merged_item = {**item1, **item2}
#             merged_map.append(merged_item)

    
#     return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
# @app.route('/account7')
# def account7Index():
#     key = key7
#     secret = secret7
#     # Your API request logic here
#     secret_bytes = bytes(secret, encoding='utf-8')
#     balanceData = fetch_balance(key,secret)
#     timeStamp = int(round(time.time() * 1000))

#     body = {
#         "details": True,
#         "status": "open",
#         "size": 200,
#         "timestamp": timeStamp
#     }

#     json_body = json.dumps(body, separators=(',', ':'))

#     signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
#     print(signature)

#     url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

#     headers = {
#         'Content-Type': 'application/json',
#         'X-AUTH-APIKEY': key,
#         'X-AUTH-SIGNATURE': signature
#     }

#     response = requests.post(url, data=json_body, headers=headers)
#     data = response.json()
 
#     ticker_data = fetch_line_graph_data()
#     merged_map = []

#     for item1 in data:
#       for item2 in ticker_data:
#         if item1.get('market') == item2.get('market'):
#             merged_item = {**item1, **item2}
#             merged_map.append(merged_item)

    
#     return render_template('index.html', data={'tableData': merged_map, 'balanceData': balanceData})
@app.route('/accounts')
def allAcountsData():
    ticker_data = fetch_line_graph_data()
    merged_map = []
    for account in allAcounts:
    	data = fetchCurrentOrders(account)
    	for item1 in data:
      		for item2 in ticker_data:
        		if item1.get('market') == item2.get('market'):
            			merged_item = {**item1, **item2, 'account': account}
            			merged_map.append(merged_item)

    
    return render_template('indexAll.html', data= merged_map)
def fetchCurrentOrders(acccount):
    split_string = acccount.split("account")
    number = split_string[1]
    key_variable_name = f"key{number}"
    secret_variable_name = f"secret{number}"
    key = eval(key_variable_name)
    secret = eval(secret_variable_name)
    print(key)
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    timeStamp = int(round(time.time() * 1000))

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    
    return data
        
@app.route('/history/<account>')
def historyIndex(account):
    print(account)
    key = ""
    secret = ""
    if account == "account1":
    	key = key1
    	secret = secret1
    elif account == "account2":
    	key = key2
    	secret = secret2
    elif account == "account3":
    	key = key3
    	secret = secret3
    elif account == "account4":
    	key = key4
    	secret = secret4
    elif account == "account5":
    	key = key5
    	secret = secret5
    # elif account == "account6":
    # 	key = key6
    # 	secret = secret6
    # elif account == "account7":
    # 	key = key7
    # 	secret = secret7		
   
    # Your API request logic here
    secret_bytes = bytes(secret, encoding='utf-8')
    timeStamp = int(round(time.time() * 1000))
    balanceData = fetch_balance(key,secret)

    body = {
        "details": True,
        "status": "open",
        "size": 200,
        "status":"close",
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    print(signature)

    url = "https://api.coindcx.com/exchange/v1/margin/fetch_orders"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    for item in data:
        timestamp = item['updated_at']
        item['updated_at'] = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('indexHistory.html', data={'tableData': data})    
@app.route('/exit', methods=['POST'])
def exit_trade():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Assuming the JSON data has a 'coins' key containing a list of selected coins
        account = data.get('account')
        selected_coins = data.get('coins', [])
        resp_l = []
        print(selected_coins)
        for id in selected_coins:
            resp = exit_order(id,account)
            resp_l.append(resp)
            
            # Respond with a success message
        return jsonify({'message': 'Trade exit successful', 'coins': resp_l}), 200

    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500
@app.route('/exitAll', methods=['POST'])
def exit_all_trade():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        

        # Assuming the JSON data has a 'coins' key containing a list of selected coins
        resp_l = []
        print(data)
        for account, coins_string in data.items():
        	selected_coins = coins_string.split(', ')
        	print(account)
        	print(selected_coins)
        	for id in selected_coins:
            		resp = exit_order(id, account)
            		resp_l.append(resp)
        # Respond with a success message
        return jsonify({'message': 'Trade exit successful', 'coins': resp_l}), 200
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500
def exit_order(id,account):
    key = ""
    secret = ""
    if account == "account1":
    	key = key1
    	secret = secret1
    elif account == "account2":
    	key = key2
    	secret = secret2
    elif account == "account3":
    	key = key3
    	secret = secret3
    elif account == "account4":
    	key = key4
    	secret = secret4
    elif account == "account5":
    	key = key5
    	secret = secret5
    # elif account == "account6":
    # 	key = key6
    # 	secret = secret6
    # elif account == "account7":
    #     key = key7
    #     secret = secret7
    # python3
    secret_bytes = bytes(secret, encoding='utf-8')
    # python2
    # secret_bytes = bytes(secret)

    # Generating a timestamp.
    timeStamp = int(round(time.time() * 1000))

    body = {
        "id": id,
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/margin/exit"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    print(data)
    return data
      
#Function to fetch line graph data from the API
def fetch_line_graph_data():
    # Replace the URL with your API endpoint
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    ticker_data = response.json()

    # Filter data for a specific market, e.g., FILUSDT
    # filtered_data = next((item for item in ticker_data if item.get('market') == 'market'), None)

    # Return a tuple of timestamp and last price
   
    return ticker_data
@app.route('/coinPrice')    
def coinPrice():
    print(get_percentage_change("B-BTC_USDT"))
    # Replace the URL with your API endpoint
    url = "https://api.coindcx.com/exchange/v1/markets_details"
    response = requests.get(url)
    data = response.json()
    
    # Return a tuple of timestamp and last price
    filtered_data = [item for item in data if item.get('market') != 'BTCINR_insta' and item.get('base_currency_short_name') == 'USDT' and item.get('max_leverage') != None and item.get('max_leverage') != 0.0 ]
    ticker_data = fetch_line_graph_data()
    merged_map = []

    for item1 in filtered_data:
      for item2 in ticker_data:
        if item1.get('coindcx_name') == item2.get('market'):
            merged_item = {**item1, **item2}
            merged_map.append(merged_item)
   
    return render_template('newOrder.html', data=merged_map)
def get_percentage_change(symbol_name):
    print(symbol_name)

    # Fetching percentage change data for coins
    

    # Assume candlestick data retrieval here
    candlestick_data = fetch_candlestick_data(symbol_name)
    percentage_change_data = []

    if candlestick_data:
           five_min_close = candlestick_data[0]['close']  # Current close price (latest data)
           five_min_open = candlestick_data[0]['open']   # Open price from 5 minutes ago
           one_hour_close = candlestick_data[12]['close']   # Open price from 1 hour ago
           print(symbol_name)
           print(five_min_close)
           print(one_hour_close)

           # Calculate percentage change for last 5 minutes,
           five_min_change = ((five_min_close - five_min_open) / five_min_open) * 100

           # Calculate percentage change for last 1 hour
           one_hour_change = ((five_min_close - one_hour_close) / one_hour_close) * 100

           percentage_change_data = {
               "5_min_change": five_min_change,
               "1_hour_change": one_hour_change
           }

    return percentage_change_data

def fetch_candlestick_data(symbol):
    candlestick_response = requests.get(f"https://public.coindcx.com/market_data/candles?pair={symbol}&interval=5m")
    candlestick_data = candlestick_response.json()
    return candlestick_data


@app.route('/buyOrder', methods=['POST'])
def buyOrder():
    try:
    	paramsData = request.get_json()
    	totalUsd = float(paramsData.get('totalQuantity'))
    	market  = paramsData.get('market')
    	leverage  = float(paramsData.get('leverage'))
    	totalCoins = int(paramsData.get('totalCoins'))
    	account = paramsData.get('account')
    	print(paramsData)
    	
    	current_price = 0.0
    	data = fetch_line_graph_data()
    	for ticker in data:
	       if ticker['market'] == market:
	          current_price = float(ticker['last_price'])
	          precision = roundOfMap[market]
    	#quantity = totalUsd / current_price
    	quantity = round(totalUsd/current_price,precision)
    	print(quantity)
    	for i in range(totalCoins):
    		data = createOrder(market,quantity,leverage,account)
    		if type(data) is not list:
    				if data.get('status') == 'error':
    					return jsonify({'success': False, 'error': data.get('message')})
    	       
    	return jsonify({'success': True,'message': 'Order Buy successful'}), 200  
    except Exception as e:
        # Handle exceptions
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/buyAllOrder', methods=['POST'])
def buyAllOrder():
    try:
    	paramsData = request.get_json()
    	totalUsd = float(paramsData.get('totalQuantity'))
    	market  = paramsData.get('market')
    	leverage  = float(paramsData.get('leverage'))
    	totalCoins = int(paramsData.get('totalCoins'))
    
    	print(paramsData)
    	
    	current_price = 0.0
    	data = fetch_line_graph_data()
    	for ticker in data:
	       if ticker['market'] == market:
	          current_price = float(ticker['last_price'])
	          precision = roundOfMap[market]
    	#quantity = totalUsd / current_price
    	quantity = round(totalUsd/current_price,precision)
    	print(quantity)
    	error_message = ""
    	for account in allAcounts:
    	   try:
        	for i in range(totalCoins):
            		data = createOrder(market, quantity, leverage, account)
            		if type(data) is not list:
                		if data.get('status') == 'error':
                    			error_message += f"Account {account}: {data.get('message')}\n"
                    			break  # Exit the totalCoins loop if an error is encountered
    	   except Exception as e:
        	error_message += f"Error for Account {account}: {str(e)}\n"
    	
    	if error_message:
    		
    		return jsonify({'success': False, 'error': error_message})
    	else:
    	    	return jsonify({'success': True, 'message': 'Order Buy successful'}), 200        
    except Exception as e:
        # Handle exceptions
        print(e)
        return jsonify({'error': str(e)}), 500
		
def createOrder(market,quantity,leverage,account):
    
    key = ""
    secret = ""
    if account == "account1":
    	key = key1
    	secret = secret1
    elif account == "account2":
    	key = key2
    	secret = secret2
    elif account == "account3":
    	key = key3
    	secret = secret3
    elif account == "account4":
    	key = key4
    	secret = secret4
    elif account == "account5":
    	key = key5
    	secret = secret5
    # elif account == "account6":
    # 	key = key6
    # 	secret = secret6
    # elif account == "account7":
    # 	key = key7
    # 	secret = secret7
    secret_bytes = bytes(secret, encoding='utf-8')
    
    timeStamp = int(round(time.time() * 1000))

    body = {
         "side": "buy",
         "order_type": "market_order",
         "market": market,
         "quantity": quantity,
         "ecode": 'B',
         "leverage": leverage,
         "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators=(',', ':'))
    

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/margin/create"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
   
    return data
@app.route('/balance')    
def fetch_balance(key,secret):
    # python3
    
    secret_bytes = bytes(secret, encoding='utf-8')


    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
       "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/users/balances"

    headers = {
       'Content-Type': 'application/json',
       'X-AUTH-APIKEY': key,
       'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json();
    
    returnData=[]
    for item in data:
	    if item.get('currency') == 'USDT':
              returnData = item
              
           
    
    print(returnData);
    return returnData;
    
# Conversion function from USD to INR
def convert_usd_to_inr(amount_usd):
    c = CurrencyRates()
    return c.convert('USD', 'INR', amount_usd)

db_username = 'root'
db_password = '12345'
db_host = 'localhost'
db_name = 'crypto_data_db'
db_uri = f'mysql://{db_username}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Create an SQLAlchemy engine
engine = create_engine(db_uri)

markets_details_api = "https://api.coindcx.com/exchange/v1/markets_details"
response = requests.get(markets_details_api)
data = response.json()
df=pd.DataFrame(data)
usdt_pairs_df=df[(df.base_currency_short_name=='USDT') & (df.max_leverage>0) & (df.status=='active') ] 
usdt_pairs_df=usdt_pairs_df[['target_currency_short_name','symbol']]
usdt_pairs_df.rename(columns={'symbol':'market'}, inplace=True)
table_name='crypto_streaming_table'
# interval_list=['5']#,'10','15','30','60','120','240']
# Function to fetch data from the API
# latest_df=get_latest_api_data(usdt_pairs_df,interval_list,limit)
# latest_df = pd.DataFrame({
#             'col_1': [1, 2, 3],
#             'col_2': ['A', 'B', 'C']
#         })
# Function to periodically update the database with API data
def update_database_periodically():
    call=0
    while True:
        latest_df=get_latest_api_data(usdt_pairs_df)
        latest_df['create_dtm'] = pd.Timestamp.now()

        # Insert the latest DataFrame into the MySQL table
        latest_df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print('func call: ',call)
        print('timestamp before sleep: ',pd.Timestamp.now())
        # Sleep for a specific interval (adjust as needed)
        time.sleep(60)  # 5 sec
        print('timestamp after sleep: ',pd.Timestamp.now())
        call=call +1 
        # print('fun_call after func end',call)


# Create and start the background thread for periodic data update
background_thread = Thread(target=update_database_periodically)
background_thread.daemon = True
background_thread.start()

# Separate route to fetch data from the database and render the HTML template
@app.route('/latest_data')
def get_latest_data_from_db():
    ist_offset = timedelta(hours=5, minutes=30)
    interval_list = request.args.getlist('interval_list')[0].split(',')
    # Fetch the latest data from the MySQL database using a raw SQL query
    latest_dtm=pd.read_sql(f'select max(create_dtm) from {table_name};',con=engine).iloc[0,0]
    latest_data_df=pd.read_sql(f"select * from {table_name} where create_dtm = '{latest_dtm}'; ",con=engine)
    latest_data_df['last_price']=latest_data_df['last_price'].astype(float)
    latest_data_df=latest_data_df[['market','last_price','ist_time','change_24_hour']]
    latest_data_df.rename(columns={'last_price':'current_price','ist_time':'latest_ist_time'},inplace=True)
    # latest_data_df[f'latest_ist_time'] = pd.to_datetime(latest_data_df['latest_time'], unit='s', utc=True) + ist_offset


    all_offset_df=None
    for offset_interval in interval_list:
        # print(offset_interval,'\n\n\n')
        offset_col_prefix= offset_interval #  str(int(offset_interval)//60)

        sql_query = f"SELECT * FROM {table_name} WHERE create_dtm = (select distinct create_dtm from {table_name} where create_dtm <= '{latest_dtm}' order by 1 desc limit 1 offset {offset_interval});"  # Adjust the query as needed
        offset_df = pd.read_sql(sql=sql_query,con=engine)
        offset_df=offset_df[['market','last_price','ist_time']]
        offset_df['last_price']=offset_df['last_price'].astype(float)

        offset_df.rename(columns={'last_price':f'{offset_col_prefix}m_open_price'
                                  ,'ist_time':f'{offset_col_prefix}m_open_time'}
                                  ,inplace=True)
        # print(type(offset_interval))
        # print(type(int(offset_interval)//60))

        # offset_df[f'{offset_col_prefix}m_open_close_change']=((latest_data_df['current_price']-offset_df[f'{offset_col_prefix}m_open_price'])/offset_df[f'{offset_col_prefix}m_open_price'])

        # offset_df[f'{offset_col_prefix}m_ist_time'] = pd.to_datetime(offset_df[f'{offset_col_prefix}m_open_time'], unit='s', utc=True) + ist_offset
        temp_df=pd.merge(latest_data_df,offset_df,on='market',how='inner')
        temp_df[f'{offset_col_prefix}m_open_close_change']=((temp_df['current_price']-temp_df[f'{offset_col_prefix}m_open_price'])/temp_df[f'{offset_col_prefix}m_open_price'])
        temp_df.drop(['current_price','latest_ist_time','change_24_hour'], axis=1, inplace=True) #f'{offset_col_prefix}m_open_price',
        
        temp_df.sort_values(by=f'{offset_col_prefix}m_open_close_change', ascending=False,inplace=True)
        temp_df.reset_index(drop=True, inplace=True)
        temp_df.rename(columns={'market':f'{offset_col_prefix}market'},inplace=True)
        if all_offset_df is None:
            all_offset_df=temp_df  #[['market',f'{offset_col_prefix}m_open_close_change',f'{offset_col_prefix}m_ist_time']]
        else:
            all_offset_df=pd.concat([all_offset_df,temp_df],axis=1)
            # all_offset_df=pd.merge(all_offset_df,temp_df,on='market',how='left')
        
    # final_df=pd.merge(latest_data_df,all_offset_df,on='market',how='left')
    latest_data_df['24h_open_close_change']=latest_data_df['change_24_hour'].astype(float)/100
    latest_data_df.drop(['change_24_hour'], axis=1, inplace=True)
    latest_data_df.sort_values(by='24h_open_close_change', ascending=False,inplace=True)
    latest_data_df.reset_index(drop=True, inplace=True)
    final_df=pd.concat([latest_data_df,all_offset_df],axis=1)
    # final_df['24h_open_close_change']=latest_data_df['change_24_hour'].astype(float)/100
    # final_df.drop(['change_24_hour'], axis=1, inplace=True)
    final_df=pd.concat([final_df.head(15),final_df.tail(15)],axis=0)
    table_html = final_df.to_html(classes='table', index=False)

    # Render the HTML template with the DataFrame
    return render_template('stream_data.html', table=table_html)



if __name__ == '__main__':
    app.run(debug=True)

