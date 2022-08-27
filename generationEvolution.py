import threading
import geneticAction as GA
import snakeGame as SG
from tqdm import tqdm

class Evolution():

    def __init__(self, brainNum, generations):

        self.brainNum = brainNum
        self.brainList = GA.generate(self.brainNum, False)
        self.snakeGame = SG.SnakeGame()
        self.generations = generations
        self.gen_score = []
        self.avg = 1

    def evolve(self):
        
        for gen in tqdm(range(self.generations), disable=True):

            print("\nGenerations: " + str(gen))
            for index in tqdm(range(self.brainNum)):
                score = 0
                for _ in range(self.avg): # play four times each brain
                    score += self.snakeGame.play(self.brainList[index])
                score /= self.avg # average

                self.gen_score.append([self.brainList[index], score])

            next_gen, best_score, best_model, average_score = GA.get_next_gen(self.gen_score)
            print("Best Score: " + str(best_score))
            print("Avgerage Score: " + str(average_score))
            best_model.save("best_model.h5")

            # reset next generation
            self.brainList = next_gen
            self.gen_score = [] 
