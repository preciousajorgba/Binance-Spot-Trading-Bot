# peauliBOT @version2


<a name="buy_low_sell_high"></a>
## BUY-LOW-SELL-HIGH
This is a trading bot that trades on Binance SPOT WALLET

A Trading Bot that uses a combined Stochastic RSI(StochRSI) and EMA to buy low and sell high.



<a name="hello_disclaimer"></a>
## DISCLAIMER
I have no responsibility for any loss or hardship incurred directly or indirectly by using this code.

PLEASE MANAGE YOUR RISK LEVEL BEFORE USING MY SCRIPT.

USE IT AT YOUR OWN RISK!


<a name="what you need to do"></a>
1. You need your API KEY AND SECRET.
2. CREATE A .env file that contains your API KEY and SECRET e.g           

KEY=sjjshslu7787ryfyr7y8098jhj787
SECRET=1ythyt7876ulguig7iujbkjh8y

3. create a .gitinore file and add the .env file to it

<a name="how_it_works"></a>
## HOW-IT-WORKS

**NOTE** For example, for BTCUSDT, BTC is the base asset, USDT is the quote asset.

1. This script implements a strategy that helps you make some profit daily when the market moves up in a cycle and reinvest it in the next cycle.

2. Assuming you have a spot balance of 100 USDT in your Spot wallet and you want to trade BTC

3. When you run the script, the program will automatically purchase BTC using 100 USDT from your `SPOT WALLET` given that our algorithm signals a buy.

4. The script is programmed to sell when there is a sell signal from the indicators strategy(when stoch_k > stoch_d) or when the percentage profit is >=1.5%, which ever happens first.

5. The idea is to make some profit daily and accummulating over time.

6. It's more profitable in higher time-frames like 4h,1d etc

7. for more info, your can send an email @preciousajorgba@gmail.com
