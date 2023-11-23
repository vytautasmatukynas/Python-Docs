import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn visual
sns.set()

labels = ['GSPC500', 'FTSE100']

data = pd.read_csv("line_chart_data.csv")
# change date format and create new colunm for that changes
data['new_date'] = pd.to_datetime(data['Date'])

# slice data, start data from 2008-01-01 to 2009-01-01
data_2008 = data[(data['new_date'] >= '2008-01-01')]
data_2008 = data_2008[(data_2008['new_date'] <= '2008-06-01')]

plt.figure(figsize=(20, 8))
plt.plot(data_2008['new_date'],
         data_2008['GSPC500'],
         color='blue')

plt.plot(data_2008['new_date'],
         data_2008['FTSE100'],
         color='red')

plt.title('SnP FTSE Returns')
plt.ylabel('Returns')
plt.xlabel('Date')
plt.legend(labels=labels)

plt.savefig('line_chart.png')

plt.show()