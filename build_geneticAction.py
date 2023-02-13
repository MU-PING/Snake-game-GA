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
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


def generateModel():
    model = Sequential()
    model.add(Dense(units=18, input_shape=(24,), kernel_initializer=tf.keras.initializers.RandomUniform(-1, 1), activation='relu', bias_initializer=tf.keras.initializers.RandomUniform(-1, 1)))
    model.add(Dense(units=18, kernel_initializer=tf.keras.initializers.RandomUniform(-1, 1), activation='relu', bias_initializer=tf.keras.initializers.RandomUniform(-1, 1)))
    model.add(Dense(units=4, kernel_initializer=tf.keras.initializers.RandomUniform(-1, 1), activation='softmax', bias_initializer=tf.keras.initializers.RandomUniform(-1, 1)))
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

def get_next_gen(gen_score, next_bestSnake): #gen_score: [brain, fitness, score]
    next_gen = []
    gen_score.sort(key= lambda x: x[1], reverse=True) # sorted by fitness
    gen_score = np.array(gen_score)
    gen_score_index = np.array([i for i in range(gen_score.shape[0])])
    gen_score_fittness = gen_score[:, 1].astype('float64')
    probabilities = gen_score_fittness / np.sum(gen_score_fittness)
    
    # set bestsnake
    bestSnake = gen_score[0]
    if bestSnake[1] > next_bestSnake[1]:
        next_bestSnake = bestSnake
    next_gen.append(next_bestSnake[0])
    
    for i in range(2000):
        dad = gen_score[np.random.choice(gen_score_index, p=probabilities)][0]
        mom = gen_score[np.random.choice(gen_score_index, p=probabilities)][0]
        son = crossover(dad, mom)
        mutate(son)
        next_gen.append(son)
    
    return next_gen, next_bestSnake

    
    