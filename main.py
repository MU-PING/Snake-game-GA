import tensorflow as tf
import build_geneticAction as GA
import matplotlib.pyplot as plt
from build_snakeGame import SnakeGame
from build_gameGUI import GameGUI
from tqdm import tqdm

def do_training():
    print("Initializing generation...")
    snakeList = [GA.generateModel() for _ in tqdm(range(snakeNum))]
    snakeGUI = GameGUI("Training ", display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    all_best_score = []
    average = 10
    
    for gen in tqdm(range(generations), disable=True):
        print("\nGenerations: " + str(gen))
        
        gen_score = []
        snakeGUI.setGen(gen)
        
        for index in tqdm(range(len(snakeList))):
            snakeGUI.setSnakeNO(index)
            avg_fitness = 0
            avg_score = 0
            
            for _ in range(average):
                fitness, score = snakeGame.play(snakeList[index])
                avg_fitness += fitness
                avg_score += score
                
            avg_fitness /= average    
            avg_score /= average
            gen_score.append([snakeList[index], fitness, score])

        next_gen, best_fittness_score, best_model = GA.get_next_gen(gen_score)
        all_best_score.append(best_fittness_score)
        tf.keras.models.save_model(best_model, "bestModel.h5")
        
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
    
def do_testing():
    print("Loading Best Model...")
    bestModel = tf.keras.models.load_model("bestModel.h5", compile=False)
    snakeGUI = GameGUI("Testing ", display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    snakeGUI.setSnakeNO("BestSnake")
    fitness, score = snakeGame.play(bestModel)
    snakeGUI.loopGUI(score)
    
if __name__ == '__main__':
    training = True
    display_size = 21
    snakeNum = 200
    generations = 100
    
    if training:
        do_training()
    else:
        do_testing()
        
