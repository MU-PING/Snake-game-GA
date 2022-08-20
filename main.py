import sys
import os
from generationEvolution import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

"""
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
"""

if __name__ == '__main__':
    brainNum = 1000
    generations = 1000
    threadNum = 5

    print("Initializing generation...")
    evolution = Evolution(brainNum, generations, threadNum)
    
    print("\nEvolving...")
    evolution.evolve()
