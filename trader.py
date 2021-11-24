from TradingBot.priceTicker import symbol, buyPrice,sellprice
from TradingBot.config import *


def buy():
      market.create_limit_buy_order(symbol, 100, buyPrice)

      print(f'!!!!!!! Buying at {buyPrice}')
def buyNsell():
      market.create_limit_buy_order(symbol, 100, buyPrice)
      market.create_limit_sell_order(symbol, 100, sellprice)

def sell():
      market.create_limit_sell_order(symbol, 100, sellprice)
      print(f'!!!!!!!!Selling at {sellprice}')

def trailingStopLoss():
      stopLoss = buyPrice - (buyPrice * gainPercent)
      #market.create_limit_buy_order(symbol,amount, buyPrice)
      #market.create_limit_sell_order(symbol,amount,stopLoss)
      print(stopLoss)

