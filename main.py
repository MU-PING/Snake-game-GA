import build_geneticAction as GA
import matplotlib.pyplot as plt
from build_snakeGame import SnakeGame
from build_gameGUI import GameGUI
from tqdm import tqdm

if __name__ == '__main__':
    print("Initializing generation...")
    
    display_size = 21
    brainNum = 2000
    generations = 100
    
    brainList = GA.generate(brainNum, False)
    snakeGUI = GameGUI(display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    all_best_score = []
    all_best_fitness = []

    for gen in tqdm(range(1, generations+1), disable=True):
        print("\nGenerations: " + str(gen))
        
        gen_score = []
        for index in tqdm(range(len(brainList))):
            
            fitness, score = snakeGame.play(brainList[index], training=True)
            gen_score.append([brainList[index], fitness, score])

        next_gen, best_fittness_score, best_model = GA.get_next_gen(gen_score)
        all_best_score.append(best_fittness_score)
        best_model.save_weights("bestModel.h5")

        # reset next generation
        brainList = next_gen
    
        # plot Score Evolving
        plt.figure(figsize=(6, 5))
        plt.title("Score Evolving")
        plt.xlabel("Generation")
        plt.ylabel("Score")
        plt.plot(all_best_score, label="Best Score")
        plt.legend()
        plt.show()
        
    snakeGUI.quitGUI()