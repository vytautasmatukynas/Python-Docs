import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn visual
sns.set()

data = pd.read_csv("bar_chart_data.csv")
data

# change size of bar chart
# (lenght, height)
plt.figure(figsize=(10, 6))

# rotate and edit labels
plt.xticks(rotation = 45, fontsize=14)
plt.yticks(fontsize=14)

# add title and label names
plt.title("Cars Kistings by Brand", fontsize=25)
plt.ylabel("Number", fontsize=18)
plt.xlabel("Car Names", fontsize=18)

# create histogram
plt.bar(x=data['Brand'],
        height=data['Cars Listings'],
        color = ("darkblue"), 
        label="Cars Listings")

# activate labels and add legent
plt.legend(loc='upper center')

# save to image
plt.savefig("bar_chart_img.png", bbox_inches='tight')

# show histogram
plt.show()

