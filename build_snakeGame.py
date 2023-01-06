import random
import numpy as np
import build_gameGUI as GG

class Frames():
    
    def __init__(self, snake_position, size):
        # map 0=background 1=snake 2=apple
        self.map = np.zeros((size, size))
        self.snake_position = snake_position
        self.crashed = False
        self.apple = 0
        self.alive = 0
        self.leftstep = 100

        # direction
        self.prev_direction = 1 
        self.direction = 1

        for body in self.snake_position:
            self.map[body[0], body[1]] = 1
                    
    def set_apple(self, apple_position):
        self.apple_position = apple_position
        self.map[self.apple_position[0], self.apple_position[1]] = 2
        
class SnakeGame():
    
    def __init__(self):
        self.display_size = 31
        self.start = int(self.display_size // 2)
        self.gameGUI = GG.GameGUI(self.display_size)
        
    def play(self, brain, training):
        snake_position = [[self.start, self.start], [self.start-1, self.start], [self.start-2, self.start], [self.start-3, self.start]]
        frames = Frames(snake_position, self.display_size)
        apple_generator = self.apple_generator(frames.map)
        
        # init apple
        apple_position = next(apple_generator)
        frames.set_apple(apple_position)
        
        while frames.leftstep > 0:

            frames.alive += 1
            frames.leftstep -= 1
            
            self.gameGUI.drawFrame(frames, training)
            
            feedback_apple, feedback_snake, feedback_wall = self.sensor(frames)
            feedback = np.array(feedback_apple + feedback_snake + feedback_wall)
            
            # What's the difference between Model methods predict() and __call__()?(Google) 
            predict_direction = brain.predict(feedback.reshape(1, -1), verbose=0) # brain predict next direction
            direction = np.argmax(predict_direction, axis=1)[0]
            
            self.next_frame(frames, direction, apple_generator)

            if frames.crashed==True: break;

        return frames.apple + frames.alive

    def next_frame(self, frames, direction, apple_generator):
        if direction == 0 and frames.prev_direction!= 1:
            frames.direction = 0
        elif direction == 1 and frames.prev_direction!= 0: 
            frames.direction = 1
        elif direction == 3 and frames.prev_direction!= 2: 
            frames.direction = 3
        elif direction == 2 and frames.prev_direction!= 3: 
            frames.direction = 2

        frames.prev_direction = frames.direction

        snake_head = frames.snake_position[0].copy()
        if frames.direction == 1:    # right
            snake_head[0] += 1
        elif frames.direction == 0:  # left
            snake_head[0] -= 1
        elif frames.direction == 2:  # down
            snake_head[1] += 1
        elif frames.direction == 3:  # up
            snake_head[1] -= 1

        # collision with apple -----------------------
        if snake_head == frames.apple_position:
            frames.apple_position = next(apple_generator)
            frames.map[frames.apple_position[0], frames.apple_position[1]] = 2
            frames.apple += 100
            frames.leftstep += 100
    
        else:
            discard = frames.snake_position.pop()
            frames.map[discard[0], discard[1]] = 0

        # collision with self ----------------------------
        if snake_head in frames.snake_position[1:]:
            frames.crashed = True
            
        # collision with boundaries ----------------------------
        if snake_head[0] >= self.display_size or snake_head[0] < 0 or snake_head[1] >= self.display_size or snake_head[1] < 0:
            frames.crashed = True

        if not frames.crashed:
            frames.snake_position.insert(0, snake_head)
            frames.map[snake_head[0], snake_head[1]] = 1

    def apple_generator(self, frames_map):

        while 1:
            x = random.randrange(0, self.display_size)
            y = random.randrange(0, self.display_size)
            
            while frames_map[x, y] != 0:
                x = random.randrange(0, self.display_size)
                y = random.randrange(0, self.display_size)
            
            yield  [x, y]
    
    def sensor(self, frames):
        # 0 means no (top, topleft, topright, left, right, bottom, bottomleft, bottomright)
        feedback_apple = [0, 0, 0, 0, 0, 0, 0, 0]
        feedback_snake = [0, 0, 0, 0, 0, 0, 0, 0]
        feedback_wall = [0, 0, 0, 0, 0, 0, 0, 0]

        framesMap = frames.map
        snake_head_w = frames.snake_position[0][0]
        snake_head_h = frames.snake_position[0][1]

        # top
        for step in range(1, self.display_size):
            target = snake_head_h - step 

            if(target < 0): 
                feedback_wall[0] = 1/step
                break

            something = framesMap[snake_head_w, target]
            if something == 1 and feedback_snake[0] == 0:
                feedback_snake[0] = 1/step

            if something == 2 and feedback_apple[0] == 0:
                feedback_apple[0] = 1
            
        # topleft
        for step in range(1, self.display_size):
            target_w = snake_head_w - step 
            target_h = snake_head_h - step 

            if(target_w < 0 or target_h < 0): 
                feedback_wall[1] = 1/step
                break

            something = framesMap[target_w, target_h]
            if something == 1 and feedback_snake[1] == 0:
                feedback_snake[1] = 1/step

            if something == 2 and feedback_apple[1] == 0:
                feedback_apple[1] = 1
        
        
        # topright
        for step in range(1, self.display_size):
            target_w = snake_head_w + step 
            target_h = snake_head_h - step 

            if(target_w == self.display_size or target_h < 0): 
                feedback_wall[2] = 1/step
                break

            something = framesMap[target_w, target_h]
            if something == 1 and feedback_snake[2] == 0:
                feedback_snake[2] = 1/step

            if something == 2 and feedback_apple[2] == 0:
                feedback_apple[2] = 1

        # left
        for step in range(1, self.display_size):
            target = snake_head_w - step 

            if(target < 0): 
                feedback_wall[3] = 1/step
                break

            something = framesMap[target, snake_head_h]
            if something == 1 and feedback_snake[3] == 0:
                feedback_snake[3] = 1/step

            if something == 2 and feedback_apple[3] == 0:
                feedback_apple[3] = 1

        # right
        for step in range(1, self.display_size):
            target = snake_head_w + step 

            if(target == self.display_size): 
                feedback_wall[4] = 1/step
                break

            something = framesMap[target, snake_head_h]
            if something == 1 and feedback_snake[4] == 0:
                feedback_snake[4] = 1/step

            elif something == 2 and feedback_apple[4] == 0:
                feedback_apple[4] = 1

        # bottom
        for step in range(1, self.display_size):
            target = snake_head_h + step 

            if(target == self.display_size): 
                feedback_wall[5] = 1/step
                break

            something = framesMap[snake_head_w, target]
            if something == 1 and feedback_snake[5] == 0:
                feedback_snake[5] = 1/step

            if something == 2 and feedback_apple[5] == 0:
                feedback_apple[5] = 1
                      
        # bottomleft
        for step in range(1, self.display_size):
            target_w = snake_head_w - step 
            target_h = snake_head_h + step 

            if(target_w < 0 or target_h == self.display_size): 
                feedback_wall[6] = 1/step
                break

            something = framesMap[target_w, target_h]
            if something == 1 and feedback_snake[6] == 0:
                feedback_snake[6] = 1/step

            if something == 2 and feedback_apple[6] == 0:
                feedback_apple[6] = 1
                
        # bottomright
        for step in range(1, self.display_size):
            target_w = snake_head_w + step 
            target_h = snake_head_h + step 

            if(target_w == self.display_size or target_h == self.display_size): 
                feedback_wall[7] = 1/step
                break

            something = framesMap[target_w, target_h]
            if something == 1 and feedback_snake[7] == 0:
                feedback_snake[7] = 1/step

            elif something == 2 and feedback_apple[7] == 0:
                feedback_apple[7] = 1
        
        return feedback_apple, feedback_snake, feedback_wall