from quantopian.algorithm import attach_pipeline,pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume,SimpleMovingAverage
from quantopian.pipeline.filters.morningstar import Q1500US
from quantopian.pipeline.data import morningstar
import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import datetime as dt
from scipy import stats
import pandas as pd

def initialize(context):
    context.assets = [sid(24),sid(114),sid(351),sid(1900),sid(2853),sid(3766),sid(3951),sid(4537),sid(5061),sid(5121),sid(5692),sid(6295),sid(7671),sid(19725),sid(22876),sid(26401),sid(38650),sid(43127),sid(49610),sid(50288),sid(51937),sid(53158),sid(53179),sid(53248),sid(53271)]
    schedule_function(before_trading_start, date_rules.every_day, time_rules.market_open())
    
#calculated the hedged curve of each stock in order to trad  only based on the alpha value    
def before_trading_start(context,data):
    benchmark_prices = data.history(sid(8554),'price', 365 , '1d')
    benchmark_ret = benchmark_prices.pct_change()[1:] #market benchmark daily return
    for stock in context.assets:
        close_prices = data.history(stock,'price', 365 , '1d')
        close_ret = close_prices.pct_change()[1:] #stock daily return
        stock = close_ret.values
        spy = benchmark_ret.values
        spy_constant = sm.add_constant(spy)
        model = regression.linear_model.OLS(stock,spy_constant).fit()
        alpha , beta = model.params
        #negated the effect of the market by subtracting the beta value multiplied by the benchmark return
        hedged_curve = -1*beta*benchmark_ret + close_ret 
        hedged_std = hedged_curve.std()
        if hedged_std < 0.02:
            print("Stock is tradeable")
            # records the hedged curve mean only if the stock is not too volatile
            print(hedged_curve.mean())
        else:
            print("Stock is untradeable")
