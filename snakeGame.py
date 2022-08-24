import random
import numpy as np
import gameGUI as GG
class Frames():
    
    def __init__(self, snake_position, apple_position, size):

        self.feedback = np.zeros((size, size))
        self.snake_position = snake_position
        self.apple_position = apple_position
        self.crashed = False
        self.score = 0
        self.alive = 0
        self.leftstep = 100

        # direction
        self.prev_direction = 1 
        self.direction = 1

        # init feedback 0=background 1=snake 2=apple
        for body in self.snake_position:
            self.feedback[body[0], body[1]] = 1
        
        self.feedback[self.apple_position[0], self.apple_position[1]] = 2

class SnakeGame():

    def __init__(self):
        self.display_size = 50
        self.start = int(self.display_size / 2)
        self.gameGUI = GG.GameGUI(self.display_size)

    def play(self, brain):
        
        snake_position = [[self.start, self.start], [self.start-1, self.start], [self.start-2, self.start]]
        apple_position = self.generate_apple()
        frames = Frames(snake_position, apple_position, self.display_size)

        while frames.leftstep > 0:
            frames.alive += 1
            frames.leftstep -= 1
            feedback = frames.feedback.reshape(1, -1)
            self.gameGUI.update(frames)
            
            # What's the difference between Model methods predict() and __call__()?(Google) 
            predict_direction = brain.predict(feedback) # brain predict next direction
            direction = np.argmax(predict_direction, axis=1)[0]
            
            self.next_frame(frames, direction)

            if frames.crashed==True: break;

        return frames.score + frames.alive*0.01

    def next_frame(self, frames, direction):
        
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
            frames.apple_position = self.generate_apple() 
            frames.feedback[frames.apple_position[0], frames.apple_position[1]] = 2
            frames.score += 100
            frames.leftstep += 50
    
        else:
            discard = frames.snake_position.pop()
            frames.feedback[discard[0], discard[1]] = 0

        # collision with self ----------------------------
        if snake_head in frames.snake_position[1:]:
            frames.crashed = True

        # collision with boundaries ----------------------------
        if snake_head[0] >= self.display_size or snake_head[0] < 0 or snake_head[1] >= self.display_size or snake_head[1] < 0:
            frames.crashed = True

        if not frames.crashed:
            frames.snake_position.insert(0, snake_head)
            frames.feedback[snake_head[0], snake_head[1]] = 1

    def generate_apple(self):
        return [random.randrange(0, self.display_size), random.randrange(0, self.display_size)]
    
