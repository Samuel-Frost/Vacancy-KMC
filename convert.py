from ase.io import read
import numpy as np
import csv

#diamond = np.loadtxt('1_rel.data', skiprows=19) # 11 for ASE generated, 19 for lammps generated
#diamond = np.delete(diamond, 1, axis=1)
#
#index = diamond.T[0].astype(int)
#coords = np.delete(diamond,0, axis=1)
#
#print(index)
#print(coords)
def convert(name='1'):
    diamond = read(f'{name}_rel.lammpstrj', index='-1')
    coords = diamond.get_positions()

    with open(f'{name}_final.data', 'w') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow([(len(diamond))])
        for i, c in enumerate(coords):
            #print(i, c)
            writer.writerow([int(i+1), *c])

#np.savetxt('test_final.data', diamond, delimiter=' ', newline='\n', header='64')
