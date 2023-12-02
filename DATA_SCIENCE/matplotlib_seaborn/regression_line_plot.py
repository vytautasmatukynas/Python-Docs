import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# activate seaborn
sns.set(rc = {'figure.figsize': (9, 6)})

data = pd.read_csv("regression_line_scatter_plot.csv")

sns.regplot(x = "Payment",
            y = "Claims",
            data=data,
            scatter_kws={'color': 'blue'},
            line_kws={'color': 'red'})

plt.xlabel("Payment")
plt.ylabel("Claims")
plt.title("Sales")
plt.show()

#############################################

sns.lmplot(x = "Payment",
            y = "Claims",
            data=data,
            scatter_kws={'color': 'blue'},
            line_kws={'color': 'red'},
            height=10)

plt.xlabel("Payment")
plt.ylabel("Claims")
plt.title("Sales")

plt.savefig("reg_plot.png")

plt.show()