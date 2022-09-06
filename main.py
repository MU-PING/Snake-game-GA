import sys
from generationEvolution import *

if __name__ == '__main__':
    brainNum = 2000
    generations = 400

    print("Initializing generation...")
    evolution = Evolution(brainNum, generations)
    evolution.evolve()
