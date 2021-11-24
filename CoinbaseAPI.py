import matplotlib.pyplot as plt
import datetime
import time
import csv
import seaborn as sns
import pandas as pd
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
from TradingBot.priceData import *
import numpy as np
from scipy import signal
import os
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd

#biddata = []
#pricedata = []
#volumedata = []

#with open('bidper.csv', 'r') as csvfile:
   # bidline = csv.reader(csvfile, delimiter = ',')
  #  for row in bidline:
   #     biddata.append(row)
#with open('Price.csv', 'r') as csvfile:
 #   priceline = csv.reader(csvfile, delimiter = ',')
 #   for row in priceline:
  #      pricedata.append(row)
#with open('volume.csv', 'r') as csvfile:
 #   volumeline = csv.reader(csvfile, delimiter = ',')
 #   for row in volumeline:
#        volumedata.append(row)
#print(len(biddata), len(pricedata), len(volumedata))

bidvol = []
biddec = []

shortsymbol = 'KNC/USD'
while True:
    getCandle(shortsymbol)
    getCandle15(shortsymbol)

    orderbook = market.fetch_order_book(shortsymbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None



    time_series = closeData15
    spikes = []


    fig = go.Figure(data=go.Scatter(
        y = time_series,
        mode = 'lines'
    ))

    indices = find_peaks(time_series)[0]
    spikes.append(find_peaks(time_series)[0])
    print(len(indices))
    print(len(spikes[0]))
    print(len(closeData))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=time_series,
        mode='lines+markers',
        name='Original Plot'
    ))
    spikes = []
    fig.add_trace(go.Scatter(
        x=indices,
        y=[time_series[j] for j in indices],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            symbol='cross',

        ),
        name='Detected Peaks'
    ))

    #fig.show()
    #print(closeData)
    # Generate random data.
    rollingavg = [(x + y) / 2 for x, y in zip(closeData15, openData15)]
    data_x = time_series[-120:]
    data_y = np.array(closeData15[-120:])

    # Find peaks(max).
    peak_indexes = signal.argrelextrema(data_y, np.greater)
    peak_indexes = peak_indexes[0]

    # Find valleys(min).
    valley_indexes = signal.argrelextrema(data_y, np.less)
    valley_indexes = valley_indexes[0]

    # Plot main graph.
    (fig, ax) = plt.subplots()
    ax.plot(data_x, data_y)

    # Plot peaks.
    peak_x = peak_indexes
    peak_y = data_y[peak_indexes]
    ax.plot(peak_x, peak_y, marker='o', color='green', label="Peaks")

    # Plot valleys.
    valley_x = valley_indexes
    valley_y = data_y[valley_indexes]
    ax.plot(valley_x, valley_y, marker='o',color='red', label="Valleys")

    ax.plot(closeData15[-120:], 'b')


    #print(len(peak_indexes), len(valley_indexes))

    plt.title('Find peaks and valleys using argrelextrema()')
    plt.legend(loc='best')
    #plt.savefig('plotchart.png')
    #os.startfile('plotchart.png', "print")
    plt.show()

    #print(len(valley_y), len(peak_y))
    dip = valley_y
    tip = peak_y
    print(market.price_to_precision(shortsymbol,dip[-2]),market.price_to_precision(shortsymbol, tip[-2]))
    if bid < dip[-2]:
        print("SELL",market.price_to_precision(shortsymbol,bid),datetime.now().strftime('%H:%M:%S' ))
    if bid > dip[-2]:
        print("BUY",market.price_to_precision(shortsymbol,bid), datetime.now().strftime('%H:%M:%S' ))
    #print(dip)
    time.sleep(30)


