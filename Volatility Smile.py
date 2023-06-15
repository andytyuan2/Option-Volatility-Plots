from datetime import date
from datetime import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import cm
# X axis = time to maturity, Y axis = strike, Z axis = implied volatility
dict = {}

# TICKER
ticker = 'aapl'                                             # not case sensitive
stock = yf.Ticker(ticker)

# CALL VS PUT
callput = 1                                                 # call = 1, put = -1; in callput
if callput == 1:
    optionname = 'Calls'
elif callput == -1:
    optionname = 'Puts'

# EXPIRATION LIST
expiration = list(stock.options)

# EXPIRY DATE
date_of_exp = expiration[0]
expiry_date = dt.strptime(date_of_exp, '%Y-%m-%d').date()

# CHAIN DATA
option_info = {}
for x in expiration:
    if callput == 1:
        chaindata = stock.option_chain(x).calls
    elif callput == -1:
        chaindata = stock.option_chain(x).puts
    option_info[x] = chaindata

# OPTION EXPIRY
todays = date.today()
years = (expiry_date - todays).days/365

# STRIKES
strikes = list(option_info[date_of_exp]['strike'])

# VOLATILITY
vol = list(option_info[date_of_exp]['impliedVolatility'])

# PRICE EXTRACTION
price = stock.info['currentPrice']


plt.scatter(strikes, vol, c=vol, cmap = cm.jet)
plt.ylabel('Implied Volatility (%)')
plt.xlabel('Strikes($)')
plt.title('Volatility Smile for $'+ticker+' '+optionname+': Implied Volatility as a Function of Strike')
plt.show()
