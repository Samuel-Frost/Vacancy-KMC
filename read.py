from ase.io import read
import numpy as np
import csv
import subprocess

def read_log():
    with open('log.lammps', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1].split()
        return [float(last_line[6]), float(last_line[7])]
