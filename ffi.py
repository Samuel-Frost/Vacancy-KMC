import matplotlib.pyplot as plt
import cffi
import numpy as np

ffi = cffi.FFI()
ffi.cdef("""float get_r(bool direction, int distance, double* energies);
            float get_R(int distance);
            float get_t(int distance);
            struct kmc_data {
                double* times;
                double* distances;
                bool reached_surface;
            };
            float get_random();
            double index_times(struct kmc_data *data, size_t i);
            double index_distances(struct kmc_data *data, size_t i);
            size_t get_size(struct kmc_data *data);
            struct kmc_data *kmc_loop();
            bool get_reached_surface(struct kmc_data *data);
            int main(double* array);""")
C = ffi.dlopen("./example.so")

energies = np.loadtxt('layer.csv', delimiter=',')
new_energies = []
for i in range(len(energies.T[1:][0]*2)):
    new_energies.append(energies.T[1:][0][i])
    new_energies.append(energies.T[1:][1][i])
# so now energies is just an array indexed as
# [2*distance+0] for up [2*distance+1] for down
new_energies = np.array(new_energies, dtype=np.double)
C_energies = ffi.cast("double*", new_energies.ctypes.data)

kB = 8.6173303e-5
T=800


# print(40e12 * np.exp(-C_energies[0]/(kB*T)))
C.main(C_energies) # define our consts at the start, they stay in memory (I think)!
for _ in range(1):
    pointer = (C.kmc_loop())
    step = 1 # must be even or 1
    trunct_len = step * round( (C.get_size(pointer)-int(step/2)) / step) 
    
    appendix = C.get_size(pointer) - np.flip(np.array([i for i in range(C.get_size(pointer) - trunct_len + 1)]))[1:]
    times = np.empty(int(trunct_len/step) + len(appendix), dtype=np.double)
    distances = np.empty(int(trunct_len/step) + len(appendix), dtype=np.double)
    print(trunct_len, C.get_size(pointer))
    
    for i, j in zip(np.append(np.arange(0, trunct_len+step, step), appendix), range(int(trunct_len/step) + len(appendix))):
        times[j] =  C.index_times(pointer, i)
        distances[j] = C.index_distances(pointer, i)
    if C.get_reached_surface(pointer):
        plt.plot(times/3600, distances, 'b')
    else:
        plt.plot(times/3600, distances, 'k')
plt.show()