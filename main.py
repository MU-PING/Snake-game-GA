import tensorflow as tf
import build_geneticAction as GA
import matplotlib.pyplot as plt
from memory_profiler import profile
from build_snakeGame import SnakeGame
from build_gameGUI import GameGUI
from tqdm import tqdm

@profile
def do_training():
    print("Initializing generation...")
    snakeList = [GA.generateModel() for _ in tqdm(range(snakeNum))]
    snakeGUI = GameGUI("Training ", display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    all_best_score = [0]
    next_bestSnake = [None, 0, 0]
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
            gen_score.append([snakeList[index], avg_fitness, avg_score])

        next_gen, next_bestSnake = GA.get_next_gen(gen_score, next_bestSnake)
        tf.keras.models.save_model(next_bestSnake[0], "bestModel.h5")
        all_best_score.append(next_bestSnake[2])
        
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
    
    fitness, score = snakeGame.play(bestModel)
    snakeGUI.drawFinalText()    
    snakeGUI.maintain()
    
if __name__ == '__main__':
    training = True
    display_size = 21
    snakeNum = 1000
    generations = 200
    
    if training:
        do_training()
    else:
        do_testing()
        
