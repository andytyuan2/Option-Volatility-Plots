from datetime import date
from datetime import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain
from matplotlib import cm
from mpl_toolkits import mplot3d
# X axis = time to maturity, Y axis = strike, Z axis = implied volatility
dict = {}

# TICKER
ticker = 'aapl'                                             # not case sensitive
stock = yf.Ticker(ticker)

# CALL VS PUT
callput = -1                                                 # call = 1, put = -1; in callput
if callput == 1:
    optionname = 'Calls'
elif callput == -1:
    optionname = 'Puts'

# EXPIRATION LIST
expiration = list(stock.options)

# CHAIN DATA
option_info = {}
dte = []
strikes = []
vol = []
for x in expiration:
    if callput == 1:
        chaindata = stock.option_chain(x).calls
    elif callput == -1:
        chaindata = stock.option_chain(x).puts
    option_info[x] = chaindata
    expiry_date = dt.strptime(x, '%Y-%m-%d').date()
    dates = (expiry_date - date.today()).days
    dte.append(np.repeat(dates, len(option_info[x])))
    strikes.append((option_info[x]['strike']))
    vol.append((option_info[x]['impliedVolatility']))

strikes = list(chain(*strikes))
vol = list(chain(*vol))
dte = list(chain(*dte))

fig = plt.figure(figsize=(10,8))
axs = plt.axes(projection='3d')
axs.plot_trisurf(strikes, dte, vol, cmap=cm.jet)
axs.view_init(20,65)
plt.xlabel('Strike ($)')
plt.ylabel('Time to expiry (Days)')
axs.set_zlabel('Implied Volatility (%)')
plt.title('Volatility Surface for $'+ticker+' '+optionname+': Implied volatility as a Function of Strike and Time')
plt.show()
