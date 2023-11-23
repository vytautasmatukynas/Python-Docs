import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn visual
sns.set()
sns.set_style('white')

data = pd.read_csv("histogram_data.csv")

plt.figure(figsize=(8, 6))

plt.hist(data['Price'],
         bins=8)

plt.title("histrogram title")
plt.xlabel('price')
plt.ylabel('properties')

sns.despine()

plt.savefig('histogram.png')

plt.show()