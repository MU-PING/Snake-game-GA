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
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def generateModel():
    model = Sequential()
    model.add(Dense(units=16, input_shape=(24,), kernel_initializer='RandomNormal', activation='relu', bias_initializer='RandomNormal'))
    model.add(Dense(units=16, kernel_initializer='RandomNormal', activation='relu', bias_initializer='RandomNormal'))
    model.add(Dense(units=4, kernel_initializer='RandomNormal', activation='softmax', bias_initializer='RandomNormal'))
    return model

def crossover(dad, mom):
    dad_weight = dad.get_weights()
    mom_weight = mom.get_weights()
    son = generateModel()
    son_weight = mom.get_weights()
    
    for i in range(len(dad_weight)):
        for j in range(len(dad_weight[i])):
            if dad_weight[i][j].ndim > 0:
                for k in range(len(dad_weight[i][j])):
                    son_weight[i][j, k] = random.choice([dad_weight[i][j, k], mom_weight[i][j, k]])
                    
            else:
                son_weight[i][j] = random.choice([dad_weight[i][j], mom_weight[i][j]])
        
    son.set_weights(son_weight)
    return son

def mutate(model, mutate_rate=0.05):
    weight = model.get_weights()
    
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            if weight[i][j].ndim > 0:
                for k in range(len(weight[i][j])):
                    if random.random() < mutate_rate:                        
                        weight[i][j, k] += (random.gauss(0, 1)/5)
                    
                    # constraint weight
                    if weight[i][j, k] > 1:
                        weight[i][j, k] = 1
                    elif weight[i][j, k] < -1:
                        weight[i][j, k] = -1
            else:
                if random.random() < mutate_rate:                        
                    weight[i][j] += (random.gauss(0, 1)/5)
                
                # constraint weight
                if weight[i][j] > 1:
                    weight[i][j] = 1
                elif weight[i][j] < -1:
                    weight[i][j] = -1
                        
    # a is ndarray, a[i][j] is inefficient than a[i, j] because of new temporary array (google "numpy view vs copy")
    # a = a*2 is inefficient than a *= 2 because of new temporary array or variable

    model.set_weights(weight)

def get_next_gen(gen_score): #gen_score: [brain, fitness, score]
    gen_score.sort(key= lambda x: x[1], reverse=True) # sorted by score
    gen_score = np.array(gen_score)
    gen_score_index = np.array([i for i in range(gen_score.shape[0])])
    gen_score_fittness = gen_score[:, 1].astype('float64')
    probabilities = gen_score_fittness / np.sum(gen_score_fittness)
    
    best_model = gen_score[0][0]
    best_fittness_score = gen_score[0][2]
    
    next_gen = []
    parentsGen = 5
    for i in range(parentsGen):
        next_gen.append(gen_score[i][0])
    
    for i in range(200-parentsGen):
        dad = gen_score[np.random.choice(gen_score_index, p=probabilities)][0]
        mom = gen_score[np.random.choice(gen_score_index, p=probabilities)][0]
        next_gen.append(crossover(dad, mom))
    
    noMutationIndex = 1
    for i in range(noMutationIndex, len(next_gen)):
        mutate(next_gen[i])
    
    return next_gen, best_fittness_score, best_model

    
    