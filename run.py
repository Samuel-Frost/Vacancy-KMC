from ase.io import read
from read import read_log
from generate_structures import generate_diamond, generate_neb, find_middle
from convert import convert
from os import system as sys
#IT JUST WERKS!
import numpy as np
import matplotlib.pyplot as plt
import csv

size = [5, 5, 5]
h = size[2] # system is h * 4 tall, middle is h*2, so get h*2 worth of transitions

print("GENERATING INITIAL DIAMOND")
generate_diamond(size)
# CALL DIAMOND.IN -> relax the main structure 
print("RELAXING INITIAL DIAMOND")
sys("mpirun -np 36 lmp_mpi -in diamond.in")
print("GENERATING NEB FILES")
middle = find_middle(size)

def run(index):
    trans = generate_neb(size, index)
    print("MINIMISING NEB STRUCTURES")
    sys("mpirun -np 36 lmp_mpi -in min.in")
    print("CONVERTING TO NEB FORMAT")
    convert() # convert so it can be read by neb.in
    # CALL NEB.IN
    print("RUNNING NEB")
    sys("mpirun -np 36 lmp_mpi -partition 9x4 -in neb.in")
    return trans

def write_csv(i):
    log = read_log()
    Ebf.append(log[0])
    Ebr.append(log[1])
    #print(h, Ebf[-1], Ebr[-1])
    with open(f'layer.csv', 'a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([i, log[0], log[1]])

Ebf = []
Ebr = []

trans = run(middle)
write_csv(0)
for i in range(1, h*2-1):
    print(trans)
    trans = run(trans)
    write_csv(i)


#np.savetxt('convergence', [h, Ebf, Ebr])
plt.plot(Ebf)
plt.plot(Ebr)
plt.style.use('seaborn-v0_8')
plt.savefig('convergence.png', dpi=600)
