from django.shortcuts import render ,HttpResponse ,redirect
import yfinance as yf
import backtesting
import ta
import re
import os
import time

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.lib import SignalStrategy
from backtesting.test import SMA
import pandas as pd
from ta import momentum
from backtesting import set_bokeh_output
set_bokeh_output(notebook=False)
stl=0
tpr=0

# Create your views here.
def index(request):
    
    return render(request, 'index.html')

def next(request):
    context={
        'a': 'Crypto',
        'b': 'Stocks',
        'c': 'Currency'

    }
    return render(request, 'next.html',context)



class RSIStrategy(Strategy):
    stl=0
    tpr=0
    
    set_bokeh_output(notebook=False)
    def init(self):
        self.rsi_window = 14
        
        
        
    def next(self):
        
        close_prices = pd.Series(self.data.Close)
        price = self.data.Close[-1]
        rsi = momentum.RSIIndicator(close_prices, window=self.rsi_window).rsi()
    
        if crossover(rsi, 30):
            
            
            self.buy(sl=price - (price * int(self.stl)*0.01), tp=price +  (price * int(self.tpr)*0.01))
            
        
        elif crossover(rsi, 70):
            self.sell(sl=price + (price * int(self.stl)*0.01), tp=price -  (price * int(self.tpr)*0.01))


class SMAStrategy(Strategy):
    stl=0
    tpr=0
    def init(self):
        a=0
        
        
        

        
    
    def next(self):
        price = self.data.Close[-1]
        close_prices = pd.Series(self.data.Close)
        self.sma20 = close_prices.rolling(window=20).mean()
        self.sma30 = close_prices.rolling(window=30).mean()

        
        
        if crossover(self.sma20, self.sma30):
            print("hi")
            self.buy(sl=price - (price * int(self.stl)*0.01), tp=price +  (price * int(self.tpr)*0.01))
           
        elif crossover(self.sma30, self.sma20):
            
            self.sell(sl=price + (price * int(self.stl)*0.01), tp=price -  (price * int(self.tpr)*0.01))



def result(request):
    
    market=request.POST['market']
    asset=request.POST['asset']
    strategy=request.POST['strategy']
    tp=request.POST['tp']
    sl=request.POST['sl']
    cash=request.POST['cash']
    
    
    

   
    if(market=="Stocks"):
        asset+=".NS"
    else:
        asset+="-USD"
    x='BTC-USD'
    data = yf.download(asset, start='2020-01-01', end='2023-07-01')

    # Create a Backtest object with the RSI strategy and data
    bt = None
    set_bokeh_output(notebook=False)

    



    if(strategy=="RSI"):
        bt = Backtest(data, RSIStrategy,cash=int(cash),exclusive_orders=True)
    else:
        bt = Backtest(data, SMAStrategy,cash=int(cash),exclusive_orders=True)


    results=bt.run(stl=sl,tpr=tp)
    # Pass the backtest results to the template
    
    cwd = os.getcwd()  # Get the current working directory

    for filename in os.listdir(cwd):
        if "Strategy" in filename:
            time.sleep(1)  # Delay for 1 second
            file_path = os.path.join(cwd, filename)
            os.remove(file_path)
            print(f"Deleted file: {filename}")
            

    
    z=bt.plot()
    
    
    
    

    context = {
        'results': results,
        'start':results['Start'],
        'end':results['End'],
        'duration':results['Duration'],
        'equityfinal':results['Equity Final [$]'],
        'equitypeak':results['Equity Peak [$]'],
        'return':results['Return [%]'],
        'returnannual':results['Return (Ann.) [%]'],
        'trades':results['# Trades'],
        'winrate':results['Win Rate [%]'],
        'besttrade':results['Best Trade [%]']
        
        
    }   
    
            

    return render(request, 'results.html',context)