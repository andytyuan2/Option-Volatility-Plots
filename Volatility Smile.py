from datetime import date
from datetime import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt

# TICKER
ticker = 'aapl'                                             # not case sensitive
stock = yf.Ticker(ticker)

# CALL VS PUT
callput = 1                                                 # call = 1, put = -1; in callput

# EXPIRATION LIST
expiration = list(stock.options)
print('expiration dates are', expiration)

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


plt.scatter(strikes, vol)
plt.axvline(price)
plt.ylabel('Implied Volatility (%)')
plt.xlabel('Strikes($)')
plt.title('Volatility smile for $'+ticker+': Implied Volatility as a Function of Strike')
plt.show()
