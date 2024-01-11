#!/usr/bin/env python3
import argparse
from bacteria import *

def simulate(N, w, h):

    bac_array = []

    for i in range(N):
        bac_array.append(bacteria())

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Run-and-tumble of E. coli")

    parser.add_argument('nbac', metavar='N', type = int, help = "The amount of E. coli simulated")
    parser.add_argument('-W', '--Width', type = int, default = 2000, help = "The width of the simulation box")
    parser.add_argument('-H', '--Height', type = int, default = 2000, help = "The height of the simulation box")

    args = parser.parse_args()
    simulate(args.nbac, args.Width, args.Height)
