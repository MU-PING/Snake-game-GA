from build_evolution import Evolution

if __name__ == '__main__':
    brainNum = 1
    generations = 200

    print("Initializing generation...")
    evolution = Evolution(brainNum, generations)
    evolution.evolve()
