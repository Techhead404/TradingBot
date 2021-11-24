from TradingBot.priceData import *
from TradingBot.config import *
import ccxt

symbol = 'SHIB/USDT'
data = getCandle(symbol)
startCash = 1
a1 = 1
a2 = 2
a3 = 3
a4 = 4
a5 = 5
a6 = 6
a7 = 7

for item in closeData:
    a1 += 1
    a2 += 1
    a3 += 1
    a4 += 1
    a5 += 1
    a6 += 1
    a7 += 1

    price = (closeData[a6] + openData[a6]) / 2
    avg = (closeData[a1] + closeData[a2] + closeData[a3] + closeData[a4] + closeData[a5]) /5

    if closeData[a7] < avg:
        startCash -= 1
    if closeData[a7] > avg:
        startCash += 1


    print(startCash,market.price_to_precision(symbol,price), avg)
