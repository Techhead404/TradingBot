import ccxt
from old.config import *
import time


dates = []
openData = []
highData = []
lowData = []
closeData = []
volData = []

dates15 = []
openData15 = []
highData15 = []
lowData15 = []
closeData15 = []
volData15 = []

dates1h = []
openData1h = []
highData1h = []
lowData1h = []
closeData1h = []
volData1h = []

def getCandle(symbol):

    candles = market.fetch_ohlcv(symbol, "1m")
    del openData[0:]
    del closeData[0:]
    del highData[0:]
    del lowData[0:]
    del volData[0:]

    for candle in candles:

        openData.append(candle[1])
        highData.append(candle[2])
        lowData.append(candle[3])
        closeData.append(candle[4])
        volData.append(candle[5])

def getCandle15(symbol):

    candles = market.fetch_ohlcv(symbol, "15m")
    del openData15[0:]
    del closeData15[0:]
    del highData15[0:]
    del lowData15[0:]
    del volData15[0:]

    for candle in candles:

        openData15.append(candle[1])
        highData15.append(candle[2])
        lowData15.append(candle[3])
        closeData15.append(candle[4])
        volData15.append(candle[5])

def getCandle1h(symbol):

    candles = market.fetch_ohlcv(symbol, "1h")
    del openData1h[0:]
    del closeData1h[0:]
    del highData1h[0:]
    del lowData1h[0:]
    del volData1h[0:]

    for candle in candles:

        openData1h.append(candle[1])
        highData1h.append(candle[2])
        lowData1h.append(candle[3])
        closeData1h.append(candle[4])
        volData1h.append(candle[5])

def getBooks(symbol, params):

    orderbook = market.fetch_order_book(symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    price = (bid + ask) / 2

    if params =='price':
        return price
    if params =='bid':
        return bid
    if params == 'ask':
        return ask