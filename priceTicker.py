import time
from TradingBot.priceData import *
from datetime import datetime
import ccxt as ex
from TradingBot.config import *
#from old.priceData import closeData, closeData15, highData, lowData, openData, getBooks
import pandas as pd
#from test import text
import time
from csv import writer
import numpy as np
from scipy import signal
from scipy.signal import find_peaks
import requests


#tickName = ticker[0]
usd = market.fetch_balance()
#nBal = usd[tickName]['free']
# about = nBal
#uBal = usd['USDT']['free']
cycount = 0

def trailingStopLoss():
    usd = market.fetch_balance()
    uBal = usd[curname]['free']
    amount = (200 / price)

    if uBal > 400:
        print('Buy', symbol, "at", price, 'Time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(symbol, amount)
        print(uBal)

        market.create_market_buy_order(symbol=symbol, amount=amount)
        time.sleep(3)
        trade = market.fetch_my_trades(symbol, limit=1)

        pricePaid = trade[0]['price']

        # pricePaid = price
        output(f"{symbol}**{market.price_to_precision(symbol,pricePaid)}**{uBal}**{nBal}**{round(bidamount)}**"
               f"**{market.price_to_precision(symbol,closeData[-1])}**{market.price_to_precision(symbol,closeData[-2])}**"
               f"**{market.price_to_precision(symbol,closeData15[-1])}**{market.price_to_precision(symbol,closeData15[-2])}**"
               f"**{market.price_to_precision(symbol, closeDatah[-1])}**{market.price_to_precision(symbol, closeDatah[-1])}**"
               f"**{market.price_to_precision(symbol,closeData[-1])}**{datetime.now().strftime('%H:%M:%S')}**")
        print(pricePaid, price)

        # return pricePaid

        # usd = bina.fetch_balance()
        # nBal = usd[tickName]['free']
        # bina.create_limit_sell_order(symbol, amount=nBal, price=sellprice)


def checkBuy():
    if price <= buyPrice:
        print('checkBuy called')
        trailingStopLoss()


def checkStop():
    if price <= pricePaid / 1.021:
        print("Check Stop Called", "bidp", bidp, "askp", askp, )
        usd = bina.fetch_balance()
        nBal = usd[tickName]['free']
        if nBal > 1:
            market.create_market_sell_order(symbol=symbol, amount=nBal)

def output(dataout):
        with open('actions.csv', 'a', newline='') as f_object:
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(dataout)
            # Close the file object
            f_object.close()
def getpercent():
    orderbook = market.fetch_order_book(symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    bi = orderbook['bids']
    si = orderbook['asks']
    bidprice = []
    bidv = []
    askprice = []
    askv = []
    del askprice[0:]
    del askv[0:]
    del bidprice[0:]
    del bidv[0:]

    for item in bi:
        bidprice.append(item[0])
        bidv.append(item[1])

    for item in si:
        askprice.append(item[0])
        askv.append(item[1])

    outbound = []

    for item in askprice:
        if item < price * 1.031:
            outbound.append(item)
            askmargin = len(outbound)

    inbound = []

    for item in bidprice:
        if item < price * 1.031:
            inbound.append(item)
            bidmargin = len(inbound)

    bookask = sum(askv[0:])
    bookbid = sum(bidv[0:])
    bookVolume = (bookask + bookbid)
    bidamount = abs(((bookbid - bookVolume) / bookVolume) * 100)
    askamount = abs(((bookask - bookVolume) / bookVolume) * 100)

    askvsum = sum(askv) / len(askv)
    asksum = sum(askprice) / len(askprice)

    bidvsum = sum(bidv) / len(bidv)
    bidsum = sum(bidprice) / len(bidprice)


def datastore(dataout):
    with open('Data.csv', 'a', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(dataout)
        # Close the file object
        f_object.close()
askamount = 0
bidamount = 0

#trade = market.fetch_my_trades(symbol, limit=1)
#pricePaid = trade[0]['price']
bidcounter = 0
askcounter = 0
url = "https://www.binance.us"
timeout = 5
while True:
    #print("<><><><><><><><><><><>", datetime.now().strftime('%H:%M:%S'), "<><><><><><><><><><><><><><><>")
    for item in coinList:
        try:
            request = requests.get(url, timeout=timeout)
            #Change symbol = symbol for single and symbol = item for list
            symbol = item
            ticker = symbol.split('/', 1)
            tickName = ticker[0]
            curname = ticker[1]
            #print(curname)
            print(symbol, "<><><><><><><><><><><><><><><><><><><><><><><><><><><><>", datetime.now().strftime('%H:%M:%S'))

            getCandle(symbol,"15m")
            print(closeData[-1])
            usd = market.fetch_balance()
            nBal = usd[tickName]['free']
            uBal = usd[curname]['free']

            getCandle(symbol)

            orderbook = market.fetch_order_book(symbol)
            bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None

            price = bid
            trade = market.fetch_my_trades(symbol, limit=1)
            if len(trade) == 0:
                pricePaid = price
            else: pricePaid = trade[0]['price']

            if len(trade) != 0:
                pricePaid = trade[0]['price']

            minMax = lowData[430:] + highData[430:]
            maxPrice = max(minMax)
            minPrice = min(minMax)
            priceSpread = (maxPrice * .9999) - (minPrice * 1.0102)
            amount = (uBal / price) / 1.1
            profit = amount * priceSpread
            buyPrice = minPrice * 1.0017  # 1.0102
            stoploss = minPrice - (minPrice * .0001)
            sellprice = maxPrice * .9989

            bi = orderbook['bids']
            si = orderbook['asks']
            bidprice = []
            bidv = []
            askprice = []
            askv = []
            del askprice[0:]
            del askv[0:]
            del bidprice[0:]
            del bidv[0:]

            for item in bi:
                bidprice.append(item[0])
                bidv.append(item[1])

            for item in si:
                askprice.append(item[0])
                askv.append(item[1])

            outbound = []

            for item in askprice:
                if item < price * 1.031:
                    outbound.append(item)
                    askmargin = len(outbound)

            inbound = []

            for item in bidprice:
                if item < price * 1.031:
                    inbound.append(item)
                    bidmargin = len(inbound)

            bookask = sum(askv[0:])
            bookbid = sum(bidv[0:])
            bookVolume = (bookask + bookbid)
            bidamount = abs(((bookbid - bookVolume) / bookVolume) * 100)
            askamount = abs(((bookask - bookVolume) / bookVolume) * 100)

            askvsum = sum(askv) / len(askv)
            asksum = sum(askprice) / len(askprice)

            bidvsum = sum(bidv) / len(bidv)
            bidsum = sum(bidprice) / len(bidprice)

            getCandle15(symbol)
            trendavg1 = sum(closeData15[-4:-2])
            trendavg2 = sum(closeData15[-6:-4])
            trendavg1 = trendavg1 / len(closeData15[-4:-2])
            trendavg2 = trendavg2 / len(closeData15[-6:-4])

            perper = bidvsum + askvsum
            bidp = abs(((bidvsum - perper) / perper) * 100)
            askp = abs(((askvsum - perper) / perper) * 100)

            hourDiff = abs((min(lowData[-30:]) - max(highData[-30:])) / max(highData[-30:])) * 100
            avg_vol = sum(volData[-60:]) / len(volData[-60:])

            shortavg = (min(closeData[-60:-2]) + max(openData[-60:-2])) / 2
            shortavg2 = (min(closeData[-30:-2]) + max(openData[-30:-2])) / 2

            getCandleh(symbol)

            houravg1 = (closeDatah[-3] + openDatah[-3]) / 2
            houravg2 = (closeDatah[-2] + openDatah[-2]) / 2
            mintrend = sum(closeData[-10:-1]) / len(closeData[-10:-1])
            mintrend15 = sum(closeData15[-5:-1]) / len(closeData15[-5:-1])
            mintrend1h = sum(closeDatah[-5:-1]) / len(closeDatah[-5:-1])

            spreadper = ((min(closeData[-30:]) - max(closeData[-30:])) / max(closeData[-30:])) * 100

            lasthouravg = abs((min(closeData15[-9:-4]) + max(openData15[-9:-4]))/2)
            past_dip = min(closeData[-10:])
            past_spike = max(closeData[-10:])
            avg_past_trend = (past_dip + past_spike) / 2
            past_15avg = abs(closeData15[-2]) + abs(openData15[-2]) / 2

            if nBal * price > 10 and price > pricePaid * 1.005 and  price < (past_dip + past_spike) / 2:
                # print(symbol,"Selling on trend")
                usd = bina.fetch_balance()
                nBal = usd[tickName]['free']
                #market.create_market_sell_order(symbol, nBal)
                nBal = usd[tickName]['free']


            #print("bid count", bidcounter, "ask count", askcounter)
            if bidcounter >= 3 and price > closeData15[-3] and (nBal * price) < 25 :
                #print(symbol,"Uptrend ",market.price_to_precision(symbol, price), "bid %",round(bidamount), "ask %",round(askamount),
                    #datetime.now().strftime("%H:%M:%S"))
                #trailingStopLoss()
                bidcounter = 0

            #print("stop", pricePaid / 1.045, pricePaid)
            #print(price, pricePaid )
            nBal = usd[tickName]['free']
            if askcounter >= 2 and (nBal * price) > 11 and price > pricePaid * 1.005:
                #print(symbol,"downtrend ",market.price_to_precision(symbol, price), "bid %",round(bidamount), "ask %",round(askamount),
                #datetime.now().strftime("%H:%M:%S"))
                usd = bina.fetch_balance()
                nBal = usd[tickName]['free']
                #market.create_market_sell_order(symbol, nBal)
                nBal = usd[tickName]['free']
                #output(f"{symbol}*{market.price_to_precision(symbol,pricePaid)}*{uBal}*{nBal}*{round(askamount)}{datetime.now().strftime('%H:%M:%S')}")
                askcounter = 0

            if pricePaid * 1.006 < price and (nBal * price) > 11:
                #print(symbol, "Stoplosss", market.price_to_precision(symbol, price), "bid %", round(bidamount), "ask %",
                    #round(askamount), pricePaid / 1.002,
                    #datetime.now().strftime("%H:%M:%S"))
                usd = bina.fetch_balance()
                nBal = usd[tickName]['free']
                #market.create_market_sell_order(symbol, nBal)
                nBal = usd[tickName]['free']
                #output(
                # f"{symbol}*{market.price_to_precision(symbol, pricePaid)}*{uBal}*{nBal}*{round(askamount)}{datetime.now().strftime('%H:%M:%S')}")

            if pricePaid / 1.002 > price and (nBal * price) > 11:
                #print(symbol, "Stoplosss", market.price_to_precision(symbol, price), "bid %", round(bidamount), "ask %",
                    #round(askamount),pricePaid / 1.002,
                    #datetime.now().strftime("%H:%M:%S"))
                usd = bina.fetch_balance()
                nBal = usd[tickName]['free']
                #market.create_market_sell_order(symbol, nBal)
                nBal = usd[tickName]['free']
                #output(
                #  f"{symbol}*{market.price_to_precision(symbol, pricePaid)}*{uBal}*{nBal}*{round(askamount)}{datetime.now().strftime('%H:%M:%S')}")

            time_series = closeData15
            data_x = time_series[-120:]
            data_y = np.array(closeData15[-120:])

            # Find peaks(max).
            peak_indexes = signal.argrelextrema(data_y, np.greater)
            peak_indexes = peak_indexes[0]

            # Find valleys(min).
            valley_indexes = signal.argrelextrema(data_y, np.less)
            valley_indexes = valley_indexes[0]
        # Plot peaks.
            peak_x = peak_indexes
            peak_y = data_y[peak_indexes]

        # Plot valleys.
            valley_x = valley_indexes
            valley_y = data_y[valley_indexes]

            dip = valley_y
            tip = peak_y



        # Plot valleys.
            valley_x = valley_indexes
            valley_y = data_y[valley_indexes]

            if len(dip) >= 3 :
                print(market.price_to_precision(symbol,dip[-2]),datetime.now().strftime('%H:%M:%S'))
                rollingavg = [(x + y) / 2 for x, y in zip(closeData15, openData15)]
                sellcount = 0
                if bid < openData15[-2]:
                    print("Sell 1")
                    sellcount += 1
                if price > pricePaid * 1.005:
                    print("Sell 2 ")
                    sellcount += 1
                if (nBal * price) > 11:
                    print("Sell 3")
                    sellcount +=1
                print("Sell trend is at",sellcount, "out of 3")
                if sellcount == 3:
                    print("<><><><><><><><>SELL AT", bid,"<><><><><><><><>")

                if bid < openData15[-2] and price > pricePaid * 1.005 and (nBal * price) > 11:
                    print("SELL",market.price_to_precision(symbol,bid),datetime.now().strftime('%H:%M:%S' ))
                    usd = bina.fetch_balance()
                    nBal = usd[tickName]['free']
                    market.create_market_sell_order(symbol, nBal)
                    nBal = usd[tickName]['free']
                    time.sleep(300)

                if bid < dip[-2] and bid < dip[-3] and (nBal * price) > 11:
                    print("********Alert Sell Now********",datetime.now().strftime('%H:%M:%S'))

                if closeData15[-2] < rollingavg[-3] and price < closeData15[-2]:
                    print("********Alert Sell Now 2********",datetime.now().strftime('%H:%M:%S'))

                bidcount = 0
                if bid > dip[-2]:
                    bidcount += 1
                    print("Buy 1")
                if dip[-3] < dip[-2]:
                    bidcount += 1
                    print("Buy 2")
                if (nBal * price) < 50:
                    bidcount += 1
                    print("Buy 3")
                if bid > closeData15[-2]:
                    bidcount += 1
                    print("Buy 4")
                if bid > openData15[-1]:
                    bidcount += 1
                    print("Buy 5")
                if rollingavg[-3] < rollingavg[-2]:
                    bidcount += 1
                    print("Buy 6")

                print("Buy trend is at",bidcount, "out of 7")
                if bidcount == 5:
                    print("<><><><><><><><>BUY AT", bid,"<><><><><><><><>")
                if bid > dip[-2] and dip[-3] < dip[-2]  and bid > closeData15[-2] and bid > openData15[-1] \
                        and rollingavg[-3] > rollingavg[-2] and  (nBal * price) < 25:
                    print("BUY",market.price_to_precision(symbol,bid), datetime.now().strftime('%H:%M:%S' ))
                    #trailingStopLoss()
            else:print(symbol,"Dip not found", len(dip))
        except:
            print("!*!*!*!*!*!*!*!*!*!*!*!*!*!OFFLINE @!*!*!*!*!*!*!*!*!*!*!*!*!*!",datetime.now().strftime('%H:%M:%S' ))
            time.sleep(300)
    time.sleep(refreshRate)

