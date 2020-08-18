import numpy as np
import pandas as pd

def initialize(context):
    context.assets = # include stocks
    context.num_stocks = # indicate number of stocks
    

# returns true if the stock needs to be shorted by using bollinger bands
def check_short(stock, data):
    # attains last 20 days of prices
    prices = data.history(stock,'price', 20 , '1d')
    # attains current price
    current_price = data.current(stock,'price')
    # creates the upper bollinger band
    upper_band = np.mean(prices) + (2*np.std(prices))
    # create the lower bollinger band 
    lower_band = np.mean(prices) - (2*np.std(prices))
    # indicates that the stock is overvalued, that means that it needs to be shorted
    if current_price >= upper_band:
        return True
    else:
        return False

# determines the optimal portfolio weights of chosen stocks
def determine_portfolio_weights(context, data):
    num_ports = 15000
    all_weights = np.zeros((num_ports,len(context.num_stocks)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)
    close = # pass in a dataframe with daily closing prices of the stocks over 3 years
    log_ret = np.log(close/close.shift(1))
    
    for ind in range(num_ports):   
        # Create Random Weights
        weights = np.array(np.random.random(18))
        # Rebalance Weights
        weights = weights / np.sum(weights)
        # Save Weights
        all_weights[ind,:] = weights
        # Expected Return
        ret_arr[ind] = np.sum((log_ret.mean() * weights) *252)
        # Expected Variance
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
        # Sharpe Ratio
        sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
        location = sharpe_arr.argmax() #location of greatest sharpe value in the array
        #these are the desired weights for the portfolio using Monte Carlo Simulation
        optimized_weights = all_weights[location,:] 
        print(optimized_weights)

    for stock in context.assets:
        should_short = check_short(stock, data)
        print ("Should short: " + should_short)
