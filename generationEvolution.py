import threading
import geneticAction as GA
import snakeGame as SG
from tqdm import tqdm

class Evolution():

    def __init__(self, brainNum, generations, threadNum):

        self.brainNum = brainNum
        self.brainList = GA.generate(self.brainNum, False)
        self.snakeGame = SG.SnakeGame()
        self.generations = generations
        self.threadNum = threadNum
        self.lock = threading.Lock()
        self.num = self.brainNum // self.threadNum
        self.gen_score = []
        self.avg = 3

    def play(self, brain):
        return 20

    def subEvolve(self, brains):

        for index in range(self.num):
            score = 0
            for _ in range(self.avg): # play four times each brain
                score += self.snakeGame.play(brains[index])
            score /= self.avg # average

            self.lock.acquire()
            self.gen_score.append((brains[index], score))
            self.lock.release()

    def evolve(self):
        
        for gen in tqdm(range(self.generations), disable=True):

            threads = []
            for i in range(self.threadNum):
                thread = threading.Thread(target=self.subEvolve, args=(self.brainList[i*self.num:(i+1)*self.num],))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            next_gen, best_score, best_model = GA.get_next_gen(self.gen_score)
            #best_model.save("best_model.h5")

            # reset next generation
            self.brainList = next_gen
            self.gen_score = [] 
