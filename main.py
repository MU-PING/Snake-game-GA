import tensorflow as tf
import build_geneticAction as GA
import matplotlib.pyplot as plt
from memory_profiler import profile
from build_snakeGame import SnakeGame
from build_gameGUI import GameGUI
from tqdm import tqdm

#@profile
def do_training(average=1):
    print("Initializing generation...")
    snakeList = [GA.generateModel() for _ in tqdm(range(snakeNum))]
    snakeGUI = GameGUI("Training ", display_size)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    all_best_score = [0]
    next_bestSnake = [None, 0, 0]
    
    for gen in tqdm(range(1, generations+1), disable=True):
        print("\nGenerations: " + str(gen))
        
        gen_score = []
        snakeGUI.setGen(str(gen))
        
        for index in tqdm(range(1, len(snakeList)+1)):
            avg_fitness = 0
            avg_score = 0
            
            for avg in range(1, average+1):
                snakeGUI.setSnakeNO(str(index)+'-'+str(avg))
                fitness, score = snakeGame.play(snakeList[index-1])
                avg_fitness += fitness
                avg_score += score
                
            avg_fitness /= average    
            avg_score /= average
            gen_score.append([snakeList[index-1], avg_fitness, avg_score])

        next_gen, next_bestSnake = GA.get_next_gen(gen_score, next_bestSnake)
        tf.keras.models.save_model(next_bestSnake[0], "bestModel.h5")
        all_best_score.append(next_bestSnake[2])
        
        # reset next generation
        snakeList = next_gen
    
        # plot Score Evolving
        plt.figure(figsize=(25, 8))
        plt.title("SnakeAI Average Score Evolving")
        plt.xlabel("Evolving Generation")
        plt.ylabel("Average Score")
        plt.plot(all_best_score, 'o--', label="Best Score", ms=6, linewidth=1.5, mfc='#ff7f0e')
        plt.legend()
        plt.show()
    
    snakeGUI.quitGUI()
    
def do_testing():
    print("Loading Best Model...")
    bestModel = tf.keras.models.load_model("bestModel.h5", compile=False)
    snakeGUI = GameGUI("Testing ", display_size, 200)
    snakeGame = SnakeGame(snakeGUI, display_size)
    
    average = 10
    avg_score = 0
    for avg in range(average):
        snakeGUI.setSnakeNO('BestSnake-'+str(avg))
        _, score = snakeGame.play(bestModel)
        avg_score += score
    avg_score /= average

    snakeGUI.drawFinalText(avg_score)    
    snakeGUI.maintain()
    
if __name__ == '__main__':
    training = 1
    display_size = 21
    snakeNum = 2000
    generations = 150
    
    if training:
        do_training()
    else:
        do_testing()
        
