import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns


# activate seaborn visual
sns.set()
sns.set_style('white')


data = pd.read_csv("multiple_charts.csv")

fig, ax = plt.subplots(figsize=(10, 7))

ax.bar(data['Year'],
       data['Participants'],
       color='k')
ax.set_ylabel("Number")
ax.tick_params(axis='y',
               width=2,
               labelsize='large')
# create twin plot
ax1 = ax.twinx()
# set limits
ax1.set_ylim(0, 1)
ax1.yaxis.set_major_formatter(PercentFormatter(xmax = 1.0))
ax1.plot(data['Year'],
         data['Python Users'],
         color='red')
ax1.set_ylabel("User",
              color='red')
ax1.tick_params(axis='y',
               width=2,
               labelsize='large')

plt.savefig("multiple_charts.png")
