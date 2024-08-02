from ase.io import read, write
from os import system as sys

for i in range(1, 20):
    neb = read(f'neb_{i}.extxyz', index=':')
    for j in range(len(neb)):
        print(i, j)
        write('test.data', neb[j], format='lammps-data')
        sys("lmp_mpi -in test.in")
        
