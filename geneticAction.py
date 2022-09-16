import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
"""
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
Must be in the same file as tensorflow and before tensorflow is imported
"""

import random
import numpy as np
from tqdm import tqdm
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def generate(population, disable=True):
    brains = []
    for _ in tqdm(range(population), disable=disable):
        model = Sequential()
        model.add(Dense(units=24, input_shape=(24,), kernel_initializer='normal', activation='relu', bias_initializer='normal'))
        model.add(Dense(units=16, kernel_initializer='normal', activation='relu', bias_initializer='normal'))
        model.add(Dense(units=4, kernel_initializer='normal', activation='softmax', bias_initializer='normal'))
        brains.append(model)

    return brains

def crossover(mom, dad, son_population):
    mom_weight = mom.get_weights()
    dad_weight = dad.get_weights()
    son = generate(son_population)
    
    for count in range(son_population):        
        son_weight = mom.get_weights()
        for i in range(len(mom_weight)):
            for j in range(len(mom_weight[i])):
                if mom_weight[i][j].ndim > 0:
                    for k in range(len(mom_weight[i][j])):
                        son_weight[i][j, k] = random.choice([dad_weight[i][j, k], mom_weight[i][j, k]])
                else:
                    son_weight[i][j] = random.choice([dad_weight[i][j], mom_weight[i][j]])
            
        son[count].set_weights(son_weight)
    return son

def mutate(model, mutate_rate = 0.15):
    weight = model.get_weights()
    
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            if weight[i][j].ndim > 0:
                for k in range(len(weight[i][j])):
                    if random.random() < mutate_rate:                        
                        weight[i][j, k] += random.gauss(0, 0.5)
            else:
                if random.random() < mutate_rate:                        
                        weight[i][j] += random.gauss(0, 0.5)
    
    # a is ndarray, a[i][j] is inefficient than a[i, j] because of new temporary array (google "numpy view vs copy")
    # a = a*2 is inefficient than a *= 2 because of new temporary array or variable

    model.set_weights(weight)

def get_next_gen(gen_score): #gen_score: [brain, score]
    gen_score.sort(key= lambda x: x[1], reverse=True) # sorted by score
    
    best_model = gen_score[0][0]
    best_score = gen_score[0][1]
    average_score = np.mean([score[1] for score in gen_score])
    
    next_gen = []
    for i in range(20):
        next_gen.append(gen_score[i][0])
        
    #crossover no1 no2
    son = crossover(gen_score[0][0], gen_score[1][0], 50)    
    next_gen += son
    
    #crossover no1 no3
    son = crossover(gen_score[0][0], gen_score[2][0], 40)    
    next_gen += son
        
    #crossover no1 no4
    son = crossover(gen_score[0][0], gen_score[3][0], 40)    
    next_gen += son
        
    #crossover no2 no3
    son = crossover(gen_score[1][0], gen_score[2][0], 30)    
    next_gen += son
    
    #crossover no2 no4
    son = crossover(gen_score[1][0], gen_score[3][0], 20)    
    next_gen += son
        
    for i in range(len(gen_score)):
        if i > 10:
            if random.random() < 0.2: # mutate rate = 0.3
                mutate(next_gen[i])       

    return next_gen, best_score, best_model, average_score

    
    