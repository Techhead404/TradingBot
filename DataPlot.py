from old.priceData import *
from old.config import market
import matplotlib.pyplot as plt
from csv import writer
from datetime import datetime

def datastore(dataout, datato):
    with open(datato, 'a', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(dataout)
        # Close the file object
        f_object.close()

symbol = "SHIB/USDT"
bidper = []
price = []
volume = []
bidvol = []
getCandle(symbol)
low_price = min(lowData[-15:])
high_price = max(highData[-15:])
while True:
    getCandle(symbol)

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
    bookask = sum(askv[0:])
    bookbid = sum(bidv[0:])
    bookVolume = (bookask + bookbid)
    bidamount = abs(((bookbid - bookVolume) / bookVolume) * 100)
    askamount = abs(((bookask - bookVolume) / bookVolume) * 100)

    if low_price > bid:
        low_price = bid
    if high_price < bid:
        high_price = bid

    average_price = (low_price + high_price) / 2


    rollingavg = [(x + y) / 2 for x, y in zip(closeData, openData)]
    #print(rollingavg[-3:])


    bidper = round(bidamount)
    priceper = market.price_to_precision(symbol, bid)
    volume = volData[-1]
    bidvol = bidper * volume
    #datastore(f"{bidper}", 'bidper.csv')
    #datastore(f"{priceper}", 'Price.csv')
    #datastore(f"{volume}", 'volume.csv')
    #datastore(f"{bidvol}", 'bidvol.csv')
    ord = []
    ord = market.fetch_my_trades(symbol,limit=1000)
    for item in ord:
        pricepaidfor = item['price']

    plt.plot(pricepaidfor, pricepaidfor )
    #plt.scatter(bidamount, bidprice)

    plt.show()

