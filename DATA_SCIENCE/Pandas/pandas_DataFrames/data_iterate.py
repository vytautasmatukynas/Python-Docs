import pandas as pd

dict = {"vardas": ["Jonas", "Petras"],
        "score": [45, 56]}

# create DataFrame
dict_frame = pd.DataFrame(dict)
print(dict_frame)

# loop trought row of DataFrame ".iterrows", but not columns like for loop
for (index, row) in dict_frame.iterrows():
    print(index)
    print(row)
    print(row.vardas)

