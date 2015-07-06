import matplotlib
import itertools
import numpy
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

names = ['RF', 'RF-C', 'RBM', 'RF-MAE', 'RF-C-MAE', 'RBM-MAE']
y = [[0.23066833099120429, 0.2250981502871684, 0.22510251313289734, 0.22475080620457158, 0.23129667946174334], #rf
      [0.26177608709645483, 0.25687855598522891, 0.25784333267105691, 0.25610408664797163, 0.26180799611575029], #rf-c
      [0.3310391, 0.32334569, 0.32933828, 0.32229659, 0.33126688],
      [0.42165933846442827, 0.41426310297767599, 0.41157084765273316, 0.40831530143490696, 0.42089603565688449], #rf
      [0.4417393001400568, 0.43088739118225217, 0.41778849839014193, 0.42864298594663713, 0.43509505642982033], #rf-c
      [0.3310391, 0.32334569, 0.32933828, 0.32229659, 0.33126688]] #rbm


linestyle = '-'
x = [1, 2, 3, 4, 5]
labels = ['FOLD 1', 'FOLD 2', 'FOLD 3', 'FOLD 4', 'FOLD 5']


plt.xlabel("Recall")
plt.ylabel("Interpolated Precision")
marker = itertools.cycle(("o","x","D","s","^",",","+",".","<",">"))

for p in y:    
    plt.plot(x, p, linestyle='--', linewidth=1.5, marker=marker.next())
plt.legend(names)

plt.xticks(x, labels, rotation='vertical')
plt.show()
#plt.savefig('foo.png', bbox_inches='tight')


