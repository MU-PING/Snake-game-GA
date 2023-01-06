import build_geneticAction as GA
import build_snakeGame as SG
import matplotlib.pyplot as plt
from tqdm import tqdm


class Evolution():
    
    def __init__(self, brainNum, generations):
        self.brainNum = brainNum
        self.brainList = GA.generate(self.brainNum, False)
        self.snakeGame = SG.SnakeGame()
        self.generations = generations
        self.gen_score = []
        self.avg = 10

    def evolve(self):
        all_best_score = []
        all_average_score = []
        
        for gen in tqdm(range(1, self.generations+1), disable=True):

            print("\nGenerations: " + str(gen))
            for index in tqdm(range(len(self.brainList))):
                
                score = 0
                for _ in range(self.avg): # play four times each brain
                    score += self.snakeGame.play(self.brainList[index], training=True)
                score /= self.avg # average

                self.gen_score.append([self.brainList[index], score])

            next_gen, best_score, best_model, average_score = GA.get_next_gen(self.gen_score)
            
            print("Best Score: " + str(best_score))
            print("Avgerage Score: " + str(average_score))
            all_best_score.append(best_score)
            all_average_score.append(average_score)
            best_model.save_weights("bestModel.h5")

            # reset next generation
            self.brainList = next_gen
            self.gen_score = [] 
        
            plt.figure(figsize=(8, 5))
            plt.title("Score Evolving")
            plt.xlabel("Generation")
            plt.ylabel("Score")
            plt.plot(all_best_score, label="Best Score")
            plt.plot(all_average_score, label="Average Score")
            plt.legend()
            plt.show()
        
        