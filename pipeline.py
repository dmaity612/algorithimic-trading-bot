from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import Q1500US
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.factors import SimpleMovingAverage, AverageDollarVolume

#how to get top 2% of tech companies in terms of Average Dollar Volume
def make_pipeline():
    
    # Base universe filter.
    base_universe = Q1500US()
    
    # Tech Sector Classifier as Filter
    sector = morningstar.asset_classification.morningstar_sector_code.latest
    #Change sector as needed (311 - tech)
    tech_sector = sector.eq(311)
    
    # Masking Base Tech Stocks
    base_tech = base_universe & tech_sector
    
    # Dollar volume factor
    dollar_volume = AverageDollarVolume(window_length=30)

    # Top half of dollar volume filter
    high_dollar_volume = dollar_volume.percentile_between(98,100)
    
    # Final Filter Mask
    top_half_base_tech = base_tech & high_dollar_volume
    
    # get close prices
    close = USEquityPricing.close.latest

    positive = close > 0
    
    # Filter for the securities that we want to analyze in order to determine if they are tradeable.    
    securities_to_trade = top_half_base_tech & positive
    
    return Pipeline(
        columns={
            'close': close,
        },
        screen=securities_to_trade
    )