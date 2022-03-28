import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as curve_fit
import scipy.constants as syc

# Aufgabe362.e
print('aufgabe362e')

data_e = np.loadtxt("aufgabe362e.txt", dtype='float', skiprows=0)
# print(data_e_raw)

rows = ["1", "2", "3", "4", "5"]
columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# ds = 0.52

# for i in range(len(rows)):
# for j in range(len(columns)):
# if data_e_raw[i,j] == 0:
#    data_e_raw[i,j] = data_e_raw[i,j]
#  else:
# data_e_raw[i,j] = data_e_raw[i,j] -ds

# data_e = np.round(data_e_raw,2)
# print(data_e)

fig, ax = plt.subplots()
im = ax.imshow(data_e, cmap='plasma')

ax.set_xticks(np.arange(len(columns)))
ax.set_yticks(np.arange(len(rows)))

ax.set_xticklabels(columns)
ax.set_yticklabels(rows)

cbarlabel = "Bildausleuchtung in lx"
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(rows)):
    for j in range(len(columns)):
        text = ax.text(j, i, data_e[i, j], ha="center", va="center", color="w")
ax.set_title("Bildausleuchtung dünne Kondensorlinse")
fig.tight_layout()
plt.show()
