import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn visual
sns.set()
sns.set_style('white')



data = pd.read_csv("area_chart_data.csv")
colors = ['#011638', '#7e2987', '#ef2026']
labels=['Diesel', 'Petrol', 'Gas']

plt.figure(figsize=(12, 8))

plt.stackplot(data['Year'],
              data['Diesel'],
              data['Petrol'],
              data["Gas"],
              colors=colors,
              edgecolor='none')

plt.xticks(data['Year'], rotation=90)
plt.legend(labels=labels, loc="upper left")
plt.ylabel('NUmber of Cars')
plt.title("Populiarity")

# remove border
sns.despine()

plt.savefig('area_chart.png')

plt.show()