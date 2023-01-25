import build_geneticAction as GA
import matplotlib.pyplot as plt
from build_snakeGame import SnakeGame
from build_gameGUI import GameGUI
from tqdm import tqdm

if __name__ == '__main__':
    training = True    
    display_size = 17
    snakeNum = 2000
    generations = 100
    
    print("Initializing generation...")
    snakeList = GA.generate(snakeNum, False)
    snakeGUI = GameGUI("Train ", display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    all_best_score = []
    all_best_fitness = []
    
    for gen in tqdm(range(generations), disable=True):
        print("\nGenerations: " + str(gen))
        
        gen_score = []
        snakeGUI.setGen(gen)
        
        for index in tqdm(range(len(snakeList))):
            
            snakeGUI.setSnakeNO(index)
            fitness, score = snakeGame.play(snakeList[index])
            gen_score.append([snakeList[index], fitness, score])

        next_gen, best_fittness_score, best_model = GA.get_next_gen(gen_score)
        all_best_score.append(best_fittness_score)
        best_model.save_weights("bestModel.h5")

        # reset next generation
        snakeList = next_gen
    
        # plot Score Evolving
        plt.figure(figsize=(7, 5))
        plt.title("Score Evolving")
        plt.xlabel("Generation")
        plt.ylabel("Score")
        plt.plot(all_best_score, label="Best Score")
        plt.legend()
        plt.show()
        
    snakeGUI.quitGUI()