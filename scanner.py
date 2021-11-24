#from old.priceTicker import *
from TradingBot.priceData import *
from csv import writer
from datetime import datetime


symbol = "MANA/USD"
while True:
    getCandle(symbol)
    getCandle15(symbol)
    getCandle1h(symbol)
    #getBooks(symbol)

    orderbook = market.fetch_order_book(symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    price = bid

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

    lastdip = min(closeData[-10:])
    lastspike = max(closeData[-10:])
    uptrendbottom = ((lastspike - lastdip) / 3) + lastdip
    print("Uptrend bottom",uptrendbottom)



    mintrend = sum(closeData[-10:]) / len(closeData[-10:])
    mintrend15 = sum(closeData15[-5:]) / len(closeData15[-5:])
    mintrend1h = sum(closeData1h[-5:]) / len(closeData1h[-5:])

    print("Price", price, "     Current Open",openData[-1], "      BidAmount", bidamount, "     Time", datetime.now().strftime("%H:%M:%S") )

    if price > openData[-1] and closeData[-2] < openData [-2]:
        print("Dip Buy at ",round(bidamount), datetime.now().strftime("%H:%M:%S") )

    if  openData[-4] > closeData[-4] and openData[-3] > closeData[-3] and openData[-3] <= closeData[-2] and price > openData[-1]:
        print("*****tooth bottom*******", round(bidamount),datetime.now().strftime("%H:%M:%S") )
#checking to find 15 minute uptrend for save time frame.

    if mintrend < price:
        print("!!!!!!!!!!!!!!!!!!Uptrend!!!!!!!!!!!!!!!!!!!", round(bidamount))
    if mintrend15 < price:
        print("****************Uptrend 15**************",round(bidamount))
    if mintrend1h < price:
        print("<<<<<<<<<<<<<<<<<<<<Uptrend 1h>>>>>>>>>>>>>>",round(bidamount))

    past_dip = min(closeData[-10:])
    past_spike = max(closeData[-10:])

    if price < past_dip:
        print("Under Dip",past_dip , "%", bidamount, "Price", price)
    if price > past_spike:
        print("Over spike", past_spike ,"%", askamount, "Price", price)
    if price > (past_dip + past_spike) / 2:
        print("Uptrend on high and low")
    if price < (past_dip + past_spike) / 2:
        print("DownTrend on high and low")
    time.sleep(15)





