import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn visual
sns.set()
sns.set_style('white')

data = pd.read_csv("scatter_data.csv")

scatter = plt.scatter(data['Area (ft.)'],
            data['Price'],
            # transparency level
            alpha=0.6,
            # color according to third variable
            c=data['Building Type'],
            cmap="viridis")

plt.legend(*scatter.legend_elements(),
           loc="upper left",
           title="Building Type")

plt.title("Relationship between Area and Price")
plt.xlabel("Area")
plt.ylabel("Price")


sns.despine()

plt.savefig("scatter_plot.png")

plt.show

# with SEABORN
plt.figure(figsize=(12, 8))
sns.scatterplot(data=data, 
                x='Price', 
                y='Area (ft.)', 
                hue='Building Type', 
                palette=['black', 'darkblue', 'purple', 'pink', 'black'], 
                s=100)

plt.title("Relationship between Area and Price")
plt.xlabel("Area")
plt.ylabel("Price")

sns.despine()

plt.savefig("scatter_plot.png")

plt.show