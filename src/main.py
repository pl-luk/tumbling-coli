#!/usr/bin/env python3
import argparse
from bacteria import *

def simulate(N, t, v, tau, alpha):

    bac_array = []

    for i in range(N):
        bac_array.append(bacteria(v, alpha, tau))

    i = 0
    
    while i < N:
    
        for bac in bac_array:
            if bac.total_runtime < t:

                bac.step()
                i += 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Run-and-tumble of E. coli")
    parser.add_argument("nbac", metavar = "N", type = int, help = "The amount of E.coli simulated")
    parser.add_argument("time", metavar = "t", type = float, help = "The simulation time in seconds")
    parser.add_argument("-v", "--velocity", type = float, default = 20., help = "The velocity of the bacteria in micrometers per second")
    parser.add_argument("-t", "--tau", type = float, default = 1, help = "The mean runtime")
    parser.add_argument("-a", "--alpha", type = float, default = np.deg2rad(70), help = "The mean turning angle")

    args = parser.parse_args()
    simulate(args.nbac, args.time, args.velocity, args.tau, args.alpha)
