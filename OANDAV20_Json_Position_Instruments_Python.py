import oandapyV20
import requests
import json
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
accountID = "xxx-xxx-xxxxxxxx-xxx"


def open_position(units):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    payload = {
        'order': {
            'units': units,
            'instrument': 'EUR_USD',
            'timeInForce': 'FOK',
            'type': 'MARKET',
            'positionFill': 'DEFAULT',
          }
        }

    url = 'https://api-fxpractice.oanda.com/v3/accounts/'+accountID+'/orders'

    response = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    print(response)

def position_details():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    url = 'https://api-fxpractice.oanda.com/v3/accounts/'+accountID+'/positions/EUR_USD'

    response = requests.get(url, headers=headers)
    output = response.json()

    output_txt = str(output).split("'")

    print(output_txt)
    print("+-- RECAP POSITION: --+")

    d = {'col1': [output_txt[3], output_txt[13], output_txt[17], output_txt[21], output_txt[43], output_txt[47], output_txt[59], output_txt[63], output_txt[67], output_txt[87], output_txt[91], output_txt[95]], 'col2': [output_txt[5], output_txt[15], output_txt[19], output_txt[23], output_txt[45], output_txt[49], output_txt[61], output_txt[65], output_txt[69], output_txt[89], output_txt[93], output_txt[97]]}
    df = pd.DataFrame(data=d)
    print(df)
    

def close_position(short_or_long):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    payload = {short_or_long: 'ALL'}

    url = 'https://api-fxpractice.oanda.com/v3/accounts/'+accountID+'/positions/EUR_USD/close'

    response = requests.put(url, headers=headers, data=json.dumps(payload)).json()
    print(response)

def prices():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    url = 'https://api-fxpractice.oanda.com/v3/accounts/'+accountID+'/pricing?instruments=EUR_USD'

    response = requests.get(url, headers=headers).json()
    print(response)
    new_response = str(response).split("'")

    d = {'col1': [new_response[11], new_response[15], new_response[23], new_response[31], new_response[35]], 'col2': [new_response[13], new_response[19], new_response[27], new_response[33], new_response[37]]}
    df = pd.DataFrame(data=d)
    print(df)

def current_candle():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    url = 'https://api-fxpractice.oanda.com/v3/accounts/'+accountID+'/instruments/EUR_USD/candles?count=1&price=M&granularity=M30'

    response = requests.get(url, headers=headers).json()
    print(response)
    new_candle = str(response).split("'")
    print(new_candle)

    d = {'col1': [new_candle[1], new_candle[5], new_candle[15], new_candle[21], new_candle[25], new_candle[29], new_candle[33]], 'col2': [new_candle[3], new_candle[7], new_candle[17], new_candle[23], new_candle[27], new_candle[31], new_candle[35]]}
    df = pd.DataFrame(data=d)
    print(df)

def candle_for_computation(diff_list):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    url = 'https://api-fxpractice.oanda.com/v3/accounts/'+accountID+'/instruments/EUR_USD/candles?count=50&price=M&granularity=M30'

    response = requests.get(url, headers=headers).json()
    new_candles = str(response).split("'")


    d = {'Time': [new_candles[-20], new_candles[-46], new_candles[-72], new_candles[-98], new_candles[-124], new_candles[-150], new_candles[-176], new_candles[-202], new_candles[-228], new_candles[-254], new_candles[-280], new_candles[-306], new_candles[-332], new_candles[-358], new_candles[-384], new_candles[-410], new_candles[-436], new_candles[-462], new_candles[-488], new_candles[-514], new_candles[-540], new_candles[-566], new_candles[-592], new_candles[-618], new_candles[-644], new_candles[-670], new_candles[-696], new_candles[-722], new_candles[-748], new_candles[-774], new_candles[-800], new_candles[-826], new_candles[-852]], 'Close Price': [new_candles[-2], new_candles[-28], new_candles[-54], new_candles[-80], new_candles[-106], new_candles[-132], new_candles[-158], new_candles[-184], new_candles[-210], new_candles[-236], new_candles[-262], new_candles[-288], new_candles[-314], new_candles[-340], new_candles[-366], new_candles[-392], new_candles[-418], new_candles[-444], new_candles[-470], new_candles[-496], new_candles[-522], new_candles[-548], new_candles[-574], new_candles[-600], new_candles[-626], new_candles[-652], new_candles[-678], new_candles[-704], new_candles[-730], new_candles[-756], new_candles[-782], new_candles[-808], new_candles[-834]]}
    df = pd.DataFrame(data=d)
    #print(df)

    #----- Prep. Computaiton MA and EMA
    d_comp = {'Close Price': [new_candles[-2], new_candles[-28], new_candles[-54], new_candles[-80], new_candles[-106], new_candles[-132], new_candles[-158], new_candles[-184], new_candles[-210], new_candles[-236], new_candles[-262], new_candles[-288], new_candles[-314], new_candles[-340], new_candles[-366], new_candles[-392], new_candles[-418], new_candles[-444], new_candles[-470], new_candles[-496], new_candles[-522], new_candles[-548], new_candles[-574], new_candles[-600], new_candles[-626], new_candles[-652], new_candles[-678], new_candles[-704], new_candles[-730], new_candles[-756], new_candles[-782], new_candles[-808], new_candles[-834]]}
    comp_df = pd.DataFrame(data=d_comp)
    

    #----- Moving Average
    ma_extract = comp_df.rolling(window=8).mean()
    ma_list = ma_extract.values.tolist()
    #print(ma_list)
    ma_extension = ma_list[7][0]
    #print("MA: ", ma_extension)

    #----- Exp. Moving Average
    cf = comp_df.sort_index(axis=0, ascending=False)
    ema_extract = cf.ewm(span=5).mean()
    ema_list = ema_extract.values.tolist()
    #print(ema_list)
    #ema = ema_list[-1]
    ema_extension = ema_list[-1][0]
    #print("EMA: ", ema_extension)
    
    #----- Diff. Calculation
    difference = (abs(float(ma_extension)-float(ema_extension))*10000)
    diff_list.append(difference)
    #print("DIFF: ", difference)
    #print(diff_list)
    

    #----- MACD
    macd_frame = comp_df.sort_index(axis=0, ascending=False)
    ema_macd12 = macd_frame.ewm(span=12).mean()
    ema_list_macd = ema_macd12.values.tolist()
    ema_extension_macd12 = ema_list_macd[-1][0]
    print("EMA12: ", ema_extension_macd12)

    ema_macd26 = macd_frame.ewm(span=26).mean()
    ema_list_macd26 = ema_macd26.values.tolist()
    ema_extension_macd26 = ema_list_macd26[-1][0]
    print("EMA26: ", ema_extension_macd26)

        #----- Substract EMA26 - EMA12
    counter = 0
    index_ema = -1
    subtraction_ema_list = []
    
    while counter < len(ema_list_macd):
        subtraction_ema = (ema_list_macd[index_ema][0]-ema_list_macd26[index_ema][0])
        subtraction_ema_list.append(subtraction_ema)
        index_ema -= 1
        counter += 1

    macd = subtraction_ema_list[0]
    print("MACD: ", macd)

        #----- EMA of macd
    
    data_macd = {'MACD': subtraction_ema_list}
    df_macd = pd.DataFrame(data=data_macd)

    macd_signal = df_macd.sort_index(axis=0, ascending=False)
    ema_signal = macd_signal.ewm(span=9).mean()
    macd_list_signal = ema_signal.values.tolist()
    signal = macd_list_signal[-1][0]
    print("Signal_MACD: ", signal)
    print(macd_list_signal)

    #----- Stochastic RSI
        #----- RSI
            #----- H
    ema_rsi = macd_frame.ewm(span=14).mean()
    ema_list_rsi = ema_rsi.values.tolist()
    ema_extension_rsi = ema_list_rsi[-1][0]
    print("EMA RSI: ", ema_extension_macd12)
    h = ema_extension_macd12

            #----- B
    b = abs(h)
    print(b)

    d_comp = {'Close Price': [new_candles[-2], new_candles[-28], new_candles[-54], new_candles[-80], new_candles[-106], new_candles[-132], new_candles[-158], new_candles[-184], new_candles[-210], new_candles[-236], new_candles[-262], new_candles[-288], new_candles[-314], new_candles[-340], new_candles[-366], new_candles[-392], new_candles[-418], new_candles[-444], new_candles[-470], new_candles[-496], new_candles[-522], new_candles[-548], new_candles[-574], new_candles[-600], new_candles[-626], new_candles[-652], new_candles[-678], new_candles[-704], new_candles[-730], new_candles[-756], new_candles[-782], new_candles[-808], new_candles[-834]]}
    comp_df = pd.DataFrame(data=d_comp)

    

    return diff_list, difference, ema_extension, ma_extension, macd, signal;
#-----------------------------------------------------------------------------------------
