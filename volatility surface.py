import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from mpl_toolkits import mplot3d
from datetime import datetime
from itertools import chain
from matplotlib import cm

ticker = 'nflx'
stock = yf.Ticker(ticker)

# maturities
maturity = list(stock.options)

# get current date
today = datetime.now().date()

Date_to_expire = []

call_data = []

for maturity in maturity:
    maturity_date = datetime.strptime(maturity, '%Y-%m-%d').date()
    Date_to_expire.append((maturity_date - today).days)
    call_data.append(stock.option_chain(maturity).calls)

strike = []
DTE_extended = []
impvol = []

for i in range(0, len(call_data)):
    strike.append(call_data[i]['strike'])
    DTE_extended.append(np.repeat(Date_to_expire[i], len(call_data[i])))
    impvol.append(call_data[i]['impliedVolatility'])

strike = list(chain(*strike))
DTE_extended = list(chain(*DTE_extended))
impvol = list(chain(*impvol))

fig = plt.figure(figsize=(7,7))
axs = plt.axes(projection='3d')
axs.plot_trisurf(strike, DTE_extended, impvol, cmap=cm.jet)
axs.view_init(30,65)
plt.xlabel('strike')
plt.ylabel('time to expiry')
plt.title('volatility surface for $'+ticker+': Implied volatility as a function of strike and time')
plt.show()



