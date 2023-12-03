import numpy as np

file = "Lending-company.csv"
data = np.loadtxt(file, delimiter=',', dtype=np.str_)
print(data)

# create numpy .npy file. npy file is more faster then .csv
np.save("new_file", data)

# load .npy file
data_2 = np.load('new_file.npy')
print(data_2)

# create numpy .npz file. npy file is more faster then .csv
# you can save few arrays to npz file
np.savez("new_file", data, data_2)
# .npz is saved with few arrays, somehting like excel sheets
data_3_npz = np.load('new_file.npz')
print(data_3_npz['arr_0'])
print(data_3_npz['arr_1'])
# can print files saved to npz
print(data_3_npz.files)

# save .csv to .txt
file = "Lending-Company-Saving.csv"
data = np.genfromtxt(file, delimiter=',', dtype=np.str_)
np.savetxt("new_file.txt", data, fmt="%s")