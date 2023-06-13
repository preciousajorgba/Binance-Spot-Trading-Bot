import websocket
import json
import os
import time
import pandas as pd
import stoch_rsi as srsi
from datetime import datetime, timedelta
from termcolor import colored
from decouple import config
from binance.client import Client
from binance.enums import *


SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"


# client keys and secret
api_key = config('KEY')
api_secret = config('SECRET')

client = Client(api_key, api_secret)



playon = False
sold = False
buy_price = 0
sell_price = 0
pair = "BTCUSDT"
quoteOrderQty = 1000



def buy(symbol, quoteOrderQty):
    try:
        print("sending  buy order")
        order = client.order_market_buy(
            symbol=symbol, quoteOrderQty=quoteOrderQty)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def sell(symbol, quantity):
    try:
        print("sending sell order")
        order = client.order_market_sell(
            symbol=symbol, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def get_data():
    dat = []
    pastdate = datetime.now() - timedelta(100)

    pastone = int(datetime.timestamp(pastdate) * 1000)

    one_klines = client.get_historical_klines(pair, "1h", str(pastone))[:-1]

    for data in one_klines:
        dlist = float(data[4])
        dat.append(dlist)

    return dat


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    global closes, playon, buy_price, sold

    
    json_message = json.loads(message)
    

    ddat = get_data()
    new_source = pd.DataFrame(ddat, columns=['close'])
    rsi, stoch_k, stoch_d = srsi.stoch_rsi_tradingview(new_source)

   
    print(stoch_k.iat[-1])
    print(stoch_d.iat[-1])

    if playon:
        if (stoch_k.iat[-1] < stoch_d.iat[-1]) or (ddat[-1] > 1.015*buy_price):

            sell_order=sell(pair, float(client.get_my_trades(
                symbol=pair)[-1]["quantity"]))
            if sell_order:
                sell_price = float(client.get_my_trades(symbol=pair)[-1]["price"])
                sold = True
                playon = False

        if (stoch_k.iat[-1] > stoch_d.iat[-1]):
            print(colored("It is oversold, but we already own it. " +
                  "We bought it at : " + str(buy_price), "green"))

    else:
        if (stoch_k.iat[-1] > stoch_d.iat[-1]):
            buy_order=buy(pair, quoteOrderQty)
            if buy_order:
                buy_price = float(client.get_my_trades(symbol=pair)[-1]["price"])
                playon = True

        else:
            if sold:
                print(colored("It is overbought, but we already sold it. " +
                      "We sold it at : " + str(sell_price), "blue"))
            else:

                print("it is overbought, but we dont own any ")


def on_error(ws, err):
    print("Got a an error: ", err)


ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
ws.run_forever()
