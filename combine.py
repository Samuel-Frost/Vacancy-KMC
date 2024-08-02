import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.style.use('seaborn-v0_8')
import tikzplotlib
from ase.io import read, write

def combine(max_neb, name):
    """
    write an extxyz file of all the rel_N.xyz files, whilst making sure not to
    show doubled frames (this will be fixed soon anyway by making last final the next initial)
    """
    combined = []
    for i in range(1, max_neb):
        neb = read(f'neb_{i}.extxyz', index=':')
        for j in range(len(neb)):
            combined.append(neb[j])
    print(len(combined))
    cut = []
    combined = combined[81:]
    y = np.loadtxt('file.txt')[81:]
    new_y = []
    for i in range(len(y) - 1):
        if abs((abs(y[i]) - abs(y[i+1]))) > 0.000001 or i >= len(y) - 6:
            new_y.append(y[i])
            cut.append(combined[i])
    y = np.append(new_y, y[-1])
    y = new_y - min(new_y)
    print(len(y))
    k = 8
    x = np.linspace(-1/k, len(y)/k, len(y))
    f = interp1d(x, y, 'cubic')
    plt.scatter(x, y)
    x = np.linspace(-0, len(y)/k, 500)
    plt.xticks([0, 2, 4, 6, 8, 10], [10, 8, 6, 4, 2, 0])
    #plt.plot(x, f(x))
    #plt.plot(x, y)
    plt.xlabel('Layer From Surface')
    plt.ylabel('Potential Energy / eV')
    plt.savefig(f'{name}.png', dpi=600)
    write(f'{name}.extxyz', cut)
    print(len(cut))
    #tikzplotlib.save('vacancy.tex')
    #print(data)
