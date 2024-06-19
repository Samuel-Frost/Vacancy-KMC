import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('layer.csv', delimiter=',')
data = data.T
plt.style.use('seaborn-v0_8')
plt.xlabel('Number of Layers Above Middle')
plt.ylabel('Energy Barrier')
plt.scatter(data[0], data[1], label='Moving Towards Surface')
plt.scatter(data[0], data[2], label='Moving Towards Bulk')
plt.legend()
plt.savefig('plot.png', dpi=600)
