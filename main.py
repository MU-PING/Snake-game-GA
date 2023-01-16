import build_geneticAction as GA
import matplotlib.pyplot as plt
from build_snakeGame import SnakeGame
from build_gameGUI import GameGUI
from tqdm import tqdm

if __name__ == '__main__':
    print("Initializing generation...")
    
    display_size = 31
    brainNum = 50
    generations = 200
    
    brainList = GA.generate(brainNum, False)
    snakeGUI = GameGUI(display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    all_best_score = []
    all_average_score = []
    avg = 10

    for gen in tqdm(range(1, generations+1), disable=True):
        print("\nGenerations: " + str(gen))
        
        gen_score = []
        for index in tqdm(range(len(brainList))):
            
            score = 0
            for _ in range(avg): # play four times each brain
                score += snakeGame.play(brainList[index], training=True)
            score /= avg # average

            gen_score.append([brainList[index], score])

        next_gen, best_score, average_score, best_model = GA.get_next_gen(gen_score)
        
        print("Best Score: " + str(best_score))
        all_best_score.append(best_score)
        
        print("Avgerage Score: " + str(average_score))
        all_average_score.append(average_score)
        
        best_model.save_weights("bestModel.h5")

        # reset next generation
        brainList = next_gen
    
        # plot Score Evolving
        plt.figure(figsize=(8, 5))
        plt.title("Score Evolving")
        plt.xlabel("Generation")
        plt.ylabel("Score")
        plt.plot(all_best_score, label="Best Score")
        plt.plot(all_average_score, label="Average Score")
        plt.legend()
        plt.show()
        
    snakeGUI.quitGUI()