import sys
from generationEvolution import *

if __name__ == '__main__':
    brainNum = 400
    generations = 120

    print("Initializing generation...")
    evolution = Evolution(brainNum, generations)
    evolution.evolve()
