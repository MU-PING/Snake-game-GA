import sys
from generationEvolution import *

if __name__ == '__main__':
    brainNum = 300
    generations = 150

    print("Initializing generation...")
    evolution = Evolution(brainNum, generations)
    evolution.evolve()
