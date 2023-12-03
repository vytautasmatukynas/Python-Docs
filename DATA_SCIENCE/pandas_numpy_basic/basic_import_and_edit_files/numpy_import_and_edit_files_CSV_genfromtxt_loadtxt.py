import numpy as np


lending_1 = np.loadtxt("Lending-Company-Numeric-Data.csv", delimiter=',')
print(lending_1)

# convert data to string with dtype
lending_1 = np.loadtxt("Lending-Company-Numeric-Data-NAN.csv", delimiter=';', dtype="<U5")
print(lending_1)

# genfromtxt can handle NAN, but it is slower
lending_2 = np.genfromtxt("Lending-Company-Numeric-Data.csv", delimiter=',')
print(lending_2)

lending_NAN = np.genfromtxt("Lending-Company-Numeric-Data-NAN.csv", delimiter=';')
print(lending_NAN)

# remove first 2 rows
lending_NAN = np.genfromtxt("Lending-Company-Numeric-Data-NAN.csv",
                            delimiter=';',
                            skip_header=2)
print(lending_NAN)

# remove last 2 rows
lending_NAN = np.genfromtxt("Lending-Company-Numeric-Data-NAN.csv",
                            delimiter=';',
                            skip_footer=2)
print(lending_NAN)

# show only 1, 3 and 2 columns
lending_NAN = np.genfromtxt("Lending-Company-Numeric-Data-NAN.csv",
                            delimiter=';',
                            usecols=(1, 3, 2))
print(lending_NAN)

# can skip columns and headers/footers
lending_NAN = np.genfromtxt("Lending-Company-Numeric-Data-NAN.csv",
                            delimiter=';',
                            usecols=(1, 3, 2),
                            skip_header=4,
                            skip_footer=2)
print(lending_NAN)

# can unpack all columns, and print all them as list
lending_NAN_1, lending_NAN_2, lending_NAN_3 = np.genfromtxt("Lending-Company-Numeric-Data-NAN.csv",
                                                            delimiter=';',
                                                            usecols=(1, 3, 2),
                                                            skip_header=4,
                                                            skip_footer=2,
                                                            unpack=True)
print(lending_NAN_1, lending_NAN_2, lending_NAN_3)