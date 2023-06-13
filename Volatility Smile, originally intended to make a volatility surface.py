import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from yahoo_fin import options as op
from yahoo_fin import stock_info as si
import yahoo_fin as yf
import yfinance as yaf
from datetime import date as date
from datetime import datetime as dt
# X axis = time to maturity, Y axis = strike, Z axis = implied volatility
dict = {}

# TICKER
ticker = 'nflx'                                             # not case sensitive

# CALL VS PUT
dict['callput'] = -1

# EXPIRATION LIST
expiration = op.get_expiration_dates(ticker)

# EXPIRY DATE
date_of_exp = expiration[0]                               
dateee = dt.strptime(date_of_exp, '%B %d, %Y').date()

if dict['callput'] == 1:                                    # call = 1, put = -1; in callput
    option_type = 'calls'
    optionsname = 'call'
elif dict['callput'] == -1:
    option_type = 'puts'
    optionsname = 'put'

# CHAIN DATA
chaindata = op.get_options_chain(ticker)[option_type]
option_info = {}
for x in expiration:
    option_info[x] = chaindata

date_expiries = []
volatility_list = []  # implied volatilities for each day of expiry, each day is a list
strikes_list = []
for dates in expiration:
    vol = []
    strikes = []
    date_expire = dt.strptime(dates, '%B %d, %Y').date()
    date_expiries.append((date_expire - date.today()).days)
    old_strike = option_info[dates][['Strike']].values.tolist()
    for n in old_strike:
        strikes.append(int(n[0]))
    strikes_list.append(strikes)
    old_vol = option_info[dates][['Implied Volatility']].values.tolist()
    for x in old_vol:
        items = x[0].replace("%","").replace(",","")
        value = float(items)
        vol.append(value)
    volatility_list.append(vol)

# length of volatility_list should reflect the expiry dates,
# length of each component should  reflect the called volatilities,
# length of strikes should reflect volatilities

price = si.get_live_price(ticker)

plt.scatter(strikes_list[0], volatility_list[0])
plt.axvline(price)
plt.ylabel('Implied Volatility (%)')
plt.xlabel('Strikes($)')
plt.show()


# I originally wanted to make a volatility surface but since the data from Yahoo finance
# only pulls from the last expiry, I am unable to effectively make use of a y-axis, 
# thus limiting my results to the closest upcoming expiry. 
# My plot then draws out a volatility smile, showing decreased implied volatility towards 
# at-the-money options for both calls and puts. 

# you may notice that some of the plots are slightly off, but as all statisticians know:
# garbage in, garbage out. No matter how my code is correct, if the data it intakes is incorrect,
# then the result will also be incorrect