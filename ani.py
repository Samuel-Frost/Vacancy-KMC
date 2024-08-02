import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from scipy.interpolate import interp1d
plt.style.use('seaborn')

y = np.loadtxt('file.txt')[81:]
new_y = []
for i in range(len(y) - 1):
    if abs((abs(y[i]) - abs(y[i+1]))) > 0.000001 or i >= len(y) - 6:
        new_y.append(y[i])
y = np.append(new_y, y[-1])
y = new_y - min(new_y)
print(len(y))
k = 8
x = np.linspace(-1/k, len(y)/k, len(y))
f = interp1d(x, y, 'cubic')

frames = 800
interval = 0.0125 * 1000

fig, ax = plt.subplots()
x = np.linspace(0, len(y)/k, frames)
plt.xticks([0, 2, 4, 6, 8, 10], [10, 8, 6, 4, 2, 0])
ax.plot(x, f(x))

plt.xlabel('Layer From Surface')
plt.ylabel('Potential Energy / eV')

line2 = ax.scatter(x[0], f(0))
#ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
ax.legend()

scat = []
for i in x:
    scat.append(f(i))

def update(frame):
    # for each frame, update the data stored on each artist.
    xi = x[frame]
    yi = scat[frame]
    data = np.stack([xi, yi]).T
    line2.set_offsets(data)
    return line2


ani = animation.FuncAnimation(fig=fig, func=update, frames=frames, interval=interval)
ani.save(filename="test.mp4", writer="ffmpeg", dpi=200)
plt.show()
