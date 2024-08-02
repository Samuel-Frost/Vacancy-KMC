from ase.io import read, write
from read import read_log
from generate_structures import generate_diamond, generate_neb, find_middle
from convert import convert
from os import system as sys
#IT JUST WERKS!
import numpy as np
import matplotlib.pyplot as plt
import csv
from combine import combine

size = [8, 8, 16]
h = size[2] # system is h * 4 tall, middle is h*2, so get h*2-2 worth of transitions
# goes from 1 -> h*2 - 1

print("GENERATING INITIAL DIAMOND")
generate_diamond(size)
# CALL DIAMOND.IN -> relax the main structure 
print("RELAXING INITIAL DIAMOND")
sys("mpirun -np 36 lmp_mpi -in diamond.in")
print("GENERATING NEB FILES")
middle = find_middle(size)

def run(index, layer_number):
    trans = generate_neb(size, index, layer_number) # all the naming is done here
    print("MINIMISING NEB STRUCTURES")
    sys("mpirun -np 36 lmp_mpi -in min.in")
    print("CONVERTING TO NEB FORMAT")
    convert() # convert so it can be read by neb.in
    # CALL NEB.IN
    print("RUNNING NEB")
    sys("mpirun -np 36 lmp_mpi -partition 9x4 -in neb.in")
    # ONCE NEB IS DONE READ IN AND REWRITE FILES WITH DIFFERENT NAME 
    struct = read('1_rel.lammpstrj', index='-1')
    write(f'rel_{layer_number * 2 - 1}.xyz', struct)
    struct = read('2_rel.lammpstrj', index='-1')
    write(f'rel_{layer_number * 2}.xyz', struct)

    traj = []
    for i in range(1, 10):
        traj.append(read(f'dump.neb.{i}', index=-1))

    write(f'neb_{layer_number}.extxyz', traj)

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

trans = run(middle, 1)
write_csv(1)
for i in range(2, h*2):
    print(trans)
    trans = run(trans, i)
    write_csv(i)


#np.savetxt('convergence', [h, Ebf, Ebr])
plt.style.use('seaborn-v0_8')
plt.plot(Ebf)
plt.plot(Ebr)
plt.savefig('8x8x16.png', dpi=600)

combine(h[2]*2, '8x8x16')
