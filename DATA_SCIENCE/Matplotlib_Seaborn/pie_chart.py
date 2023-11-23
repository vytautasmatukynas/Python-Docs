import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn
sns.set()
# seaborn color pallete
sns.set_palette('colorblind')

data = pd.read_csv("pie_chart_data.csv")
data


plt.figure(figsize=(10, 6))
plt.title('Fuel Types', 
          fontsize=16,
          fontweight='bold')

# create pie chart
plt.pie(data["Number of Cars"],
         labels=data["Engine Fuel Type"].values,
         # '.2f' - 0.00 float number, 2numbers after point
         # '%' - changed to string
         # '%%' - to show %
         autopct='%.2f%%',
         textprops={'size': "x-large",
                    'fontweight': 'bold',
                    'rotation': 45,
                    'color': 'w'})

plt.legend()

# save to image with tight layout
plt.savefig("pie_chart_img.png", bbox_inches='tight')

plt.show()