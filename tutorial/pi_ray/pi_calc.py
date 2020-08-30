# Tools for the Monte Carlo computation of Pi
import math, statistics, random, time, sys, locale
import ray
import numpy as np
import argparse



repeat=10  # We'll do this many calculations for a given N and average the results.


############################### Define Main ##############################################
def main():
    global repeat

    Ns = [500, 1000, 5000, 10000, 50000, 100000]

    parser = argparse.ArgumentParser(description="Monte Carlo Pi Calculator")
    parser.add_argument('Ns', metavar='N', type=int, default=Ns, nargs='*', help='Runs with the specified number of samples')
    parser.add_argument('-r', '--repeat', metavar='M', type=int, default=repeat, nargs='?', help='Repeat for each N, then compute average, stdev, etc')
    parser.add_argument('-l', '--local', help='Run Ray locally. Default is to join a cluster', action='store_true')

    args = parser.parse_args()
    print(f"""
            {parser.description}
            NS:             {args.Ns}
            Repeat per N:   {args.repeat}
            Run locally?    {args.local}
            """)
    repeat = args.repeat


############################### Execute Main ##############################################
if __name__ == '__main__':
    main()