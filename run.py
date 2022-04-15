import websocket, json, pprint
import config
import pandas as pd
import EMA 
import stoch_rsi as srsi
from datetime import datetime
from termcolor import colored
from binance.client import Client
from binance.enums import *




closes = []
playon=False

SOCKET = "wss://stream.binance.com:9443//dotusdt@kline_1hr"

# client keys and secret
client = Client(config.API_KEY, config.API_SECRET)

#percentage to cash out
margin_percentage = config.margin_percentage

#Trading Setup

pair,round_off = ["DOTUSDT"], [4]


def buy(symbol,quoteOrderQty):
    try:
        print("sending order")
        order = client.order_market_buy(symbol=symbol, quoteOrderQty=quoteOrderQty)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

def sell( symbol,quoteOrderQty):
    try:
        print("sending order")
        order = client.order_market_sell(symbol=symbol, quoteOrderQty=quoteOrderQty)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, playon
    

    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message["k"]

    is_candle_closed = candle['x']
    close = candle['c']
    
    if is_candle_closed:      
        closes.append(float(close))


        src=EMA.ema(EMA.ema(closes,3))

        new_source=pd.DataFrame(src, columns=['close'])

        rsi,stoch_k,stoch_d = srsi.stoch_rsi_tradingview(new_source)

        my_quote_asset = config.quote
        my_round_off = round_off[0]

        # Retrieve Current Asset INFO
        asset_info      = client.get_symbol_ticker(symbol=pair[0])
        asset_price     = float(asset_info.get("price"))
        asset_balance   = float(client.get_asset_balance(asset="DOT").get("free"))

        # Computing for Trade Quantity
        current_holding = round(asset_balance * asset_price, my_round_off)
        order_holding   = current_holding
        change_percent  = round(((current_holding - order_holding) / order_holding * 100), my_round_off)
        
        
        # Output Console and Placing Order
        if (stoch_k < stoch_d)  or (abs(change_percent) > margin_percentage): 
            if playon:
                sell(symbol=pair[0], quoteOrderQty=current_holding)
                playon=False

                print(colored(asset_info, "green"))
                print(colored("Created at           : " + str(datetime.today().strftime("%d-%m-%Y @ %H:%M:%S")), "green"))
                print(colored("Sold at         : " + str(current_holding) + " " + my_quote_asset, "green"))
                print(colored("Percentage Changed   : " + str(change_percent) + " %", "green"))
                print(colored("Action               : SELL " + str(current_holding) + " " + my_quote_asset + "\n", "green"))
            else:
                 print("It is overbought, but we don't own any. Nothing to do.")

        elif (stoch_k > stoch_d): 
            if playon:
                print("It is oversold, but you already own it, nothing to do.")
            else:

                buy(symbol=pair[0], quoteOrderQty=current_holding)
                order_holding =round(asset_balance * asset_price, my_round_off)
                playon=True
                
                print(colored(asset_info, "red"))
                print(colored("Created at           : " + str(datetime.today().strftime("%d-%m-%Y @ %H:%M:%S")), "red"))
                print(colored("Bought at          : " + str(order_holding) + " " + my_quote_asset, "red"))
                print(colored("Action               : BUY " + str(order_holding) + " " + my_quote_asset + "\n", "red"))

        else:
            print(asset_info)
            print("Created at           : " + str(datetime.today().strftime("%d-%m-%Y @ %H:%M:%S")))
            print("Current balance         : " + str(current_holding) + " " + my_quote_asset)
            print("Percentage Changed   : " + str(change_percent) + " %")
            print("Action               : Do Nothing\n")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()

