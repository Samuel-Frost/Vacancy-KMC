# two functions -> one that generates the original diamond structure to be relaxed
# -> next one that finds the midpoint for a given index -> return index of atom above vacancy
# this way we have one function (or part of the function) that finds the middle
# and another that then just does the whole thing but with just an index 
# get a naming scheme so that we can turn it into a cute movie!

from ase.spacegroup import crystal
from ase.io import read, write
import numpy as np
from  ase.neighborlist import NeighborList as neighbourlist
from ase import Atoms
centre = 5

def generate_diamond(size):
    a = 3.573211
    diamond = crystal('C', [(0, 0, 0)], size=size, spacegroup=227, cellpar=[a,a,a,90,90,90]) 
    diamond.center(5, 2)
    # is it worth just getting it working again first and then doing all the naming bollocks
    #write(f'diamond_{"_".join(str(a) for a in size)}.data', format='lammps-data')
    write(f'diamond.data', diamond, format='lammps-data')

def find_middle(size):
    """
    Returns the index of some random atom in the middle
    Returns the ParticleIdentifier-1, luckily the .data and .lammpstrj retain
    the same ParticleIdentifier, it just get jumbled up in the lammpstrj,
    but in .data ParticleIndex = ParticleIdentifier-1
    So when you want to view it in Ovito it's index+1!
    """
    global centre
    diamond = read('diamond_rel.lammpstrj', index='-1') # do we need the index?
    pos = diamond.get_positions()
    #this only works for the middle, gets worse as you get closer to the surface
    for i in range(len(pos)):
        if size[2] * 2 * 0.8925 + centre - 0.25 < pos[i][2] < size[2] * 2 * 0.8925 + centre + 0.25:
            break
    return i

def generate_neb(size, index, layer_number):
    # read in our relaxed structure
    diamond = read('diamond_rel.lammpstrj', index='-1') # do we need the index?
    bond_distance = 1.554 / 2 # may be worth checking if this is the right value
    nl = neighbourlist([bond_distance] * len(diamond), self_interaction=False, bothways=True)
    nl.update(diamond)
    # we have our index that we are concerned with, now want its neighbours
    neighbours = nl.get_neighbors(index)
    pos = diamond.get_positions()
    trans = []
    for j in neighbours[0]:
        #print(pos[j])
        if pos[j][2] - pos[index][2] > 0:
            trans.append(j)
    trans = min(trans)

    # have to get positions before indicies get fucked up
    pos_vacancy = pos[index]
    finish = diamond.copy()
    # normal start structure
    del(diamond[index])
    # vacancy is lower
    write(f'1.data', diamond, format='lammps-data')
    write(f'{layer_number * 2 - 1}.xyz', diamond)

    # move trans atom onto vacancy atom, then delete vacancy atom so indices don't get fucked up
    pos[trans] = pos_vacancy
    finish.set_positions(pos)
    del(finish[index])
    # vacancy is now higher
    write(f'2.data', finish, format='lammps-data') 
    write(f'{layer_number * 2}.xyz', finish)

    return trans
