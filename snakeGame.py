import random
import numpy as np
import gameGUI as GG

class Frames():
    
    def __init__(self, snake_position, rock_position, size):
        # map 0=background 1=snake 2=apple 3=rock
        self.map = np.zeros((size, size))
        self.snake_position = snake_position
        self.rock_position = rock_position
        self.crashed = False
        self.apple = 0
        self.alive = 0
        self.leftstep = 100

        # direction
        self.prev_direction = 1 
        self.direction = 1

        for body in self.snake_position:
            self.map[body[0], body[1]] = 1

        for rock in self.rock_position:
            for x in range(rock[0][0], rock[1][0]+1):
                for y in range(rock[0][1], rock[1][1]+1):
                    self.map[x, y] = 3
                    
    def set_apple(self, apple_position):
        self.apple_position = apple_position
        self.map[self.apple_position[0], self.apple_position[1]] = 2
        
class SnakeGame():
    
    def __init__(self):
        self.display_size = 40
        self.start = int(self.display_size / 2)
        self.gameGUI = GG.GameGUI(self.display_size)

    def play(self, brain):
        snake_position = [[self.start, self.start], [self.start-1, self.start], [self.start-2, self.start], [self.start-3, self.start]]
        rock_position = [[(8, 8), (10, 10)], [(30, 19), (31, 25)], [(8, 32), (14, 33)]]
        frames = Frames(snake_position, rock_position, self.display_size)
        
        # init apple
        apple_position = self.generate_apple(frames.map) 
        frames.set_apple(apple_position)
        
        while frames.leftstep > 0:

            frames.alive += 1
            frames.leftstep -= 1
            
            self.gameGUI.drawFrame(frames)
            
            feedback_apple, feedback_snake, feedback_rock, feedback_wall = self.sensor(frames)
            feedback = np.array(feedback_apple + feedback_snake + feedback_rock + feedback_wall)
            
            # What's the difference between Model methods predict() and __call__()?(Google) 
            predict_direction = brain.predict(feedback.reshape(1, -1), verbose=0) # brain predict next direction
            direction = np.argmax(predict_direction, axis=1)[0]
            
            self.next_frame(frames, direction)

            if frames.crashed==True: break;

        return frames.apple + frames.alive

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
            frames.apple_position = self.generate_apple(frames.map) 
            frames.map[frames.apple_position[0], frames.apple_position[1]] = 2
            frames.apple += 100
            frames.leftstep += 120
    
        else:
            discard = frames.snake_position.pop()
            frames.map[discard[0], discard[1]] = 0

        # collision with self ----------------------------
        if snake_head in frames.snake_position[1:]:
            frames.crashed = True
            
        # collision with rock ----------------------------
        for rock in frames.rock_position:
            if rock[0][0] <= snake_head[0] and snake_head[0] <= rock[1][0] and rock[0][1] <= snake_head[1] and snake_head[1] <= rock[1][1]:
                frames.crashed = True
            
        # collision with boundaries ----------------------------
        if snake_head[0] >= self.display_size or snake_head[0] < 0 or snake_head[1] >= self.display_size or snake_head[1] < 0:
            frames.crashed = True

        if not frames.crashed:
            frames.snake_position.insert(0, snake_head)
            frames.map[snake_head[0], snake_head[1]] = 1

    def generate_apple(self, frames_map):
        x = random.randrange(0, self.display_size)
        y = random.randrange(0, self.display_size)
        
        while frames_map[x, y] != 0:
            x = random.randrange(0, self.display_size)
            y = random.randrange(0, self.display_size)
        
        return [x, y]
    
    def sensor(self, frames):
        # 0 means no (top, topleft, topright, left, right, bottom, bottomleft, bottomright)
        feedback_apple = [-1, -1, -1, -1, -1, -1, -1, -1]
        feedback_snake = [-1, -1, -1, -1, -1, -1, -1, -1]
        feedback_rock = [-1, -1, -1, -1, -1, -1, -1, -1]
        feedback_wall = [-1, -1, -1, -1, -1, -1, -1, -1]

        framesMap = frames.map
        snake_head_w = frames.snake_position[0][0]
        snake_head_h = frames.snake_position[0][1]
        max_step = self.display_size

        # top
        for step in range(1, self.display_size):
            target = snake_head_h - step 

            if(target < 0): 
                feedback_wall[0] = step/max_step
                break

            something = framesMap[snake_head_w, target]
            if something == 1:
                feedback_snake[0] = step/max_step
                break

            elif something == 2:
                feedback_apple[0] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[0] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(snake_head_w, target)
            
        # topleft
        for step in range(1, self.display_size):
            target_w = snake_head_w - step 
            target_h = snake_head_h - step 

            if(target_w < 0 or target_h < 0): 
                feedback_wall[1] = step/max_step
                break

            something = framesMap[target_w, target_h]
            if something == 1:
                feedback_snake[1] = step/max_step
                break

            elif something == 2:
                feedback_apple[1] = step/max_step
                
            elif something == 3:
                feedback_rock[1] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(target_w, target_h)
                
        # topright
        for step in range(1, self.display_size):
            target_w = snake_head_w + step 
            target_h = snake_head_h - step 

            if(target_w == self.display_size or target_h < 0): 
                feedback_wall[2] = step/max_step
                break

            something = framesMap[target_w, target_h]
            if something == 1:
                feedback_snake[2] = step/max_step
                break

            elif something == 2:
                feedback_apple[2] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[2] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(target_w, target_h)

        # left
        for step in range(1, self.display_size):
            target = snake_head_w - step 

            if(target < 0): 
                feedback_wall[3] = step/max_step
                break

            something = framesMap[target, snake_head_h]
            if something == 1:
                feedback_snake[3] = step/max_step
                break

            elif something == 2:
                feedback_apple[3] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[3] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(target, snake_head_h)

        # right
        for step in range(1, self.display_size):
            target = snake_head_w + step 

            if(target == self.display_size): 
                feedback_wall[4] = step/max_step
                break

            something = framesMap[target, snake_head_h]
            if something == 1:
                feedback_snake[4] = step/max_step
                break

            elif something == 2:
                feedback_apple[4] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[4] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(target, snake_head_h)

        # bottom
        for step in range(1, self.display_size):
            target = snake_head_h + step 

            if(target == self.display_size): 
                feedback_wall[5] = step/max_step
                break

            something = framesMap[snake_head_w, target]
            if something == 1:
                feedback_snake[5] = step/max_step
                break

            elif something == 2:
                feedback_apple[5] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[5] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(snake_head_w, target)
                
                
        # bottomleft
        for step in range(1, self.display_size):
            target_w = snake_head_w - step 
            target_h = snake_head_h + step 

            if(target_w < 0 or target_h == self.display_size): 
                feedback_wall[6] = step/max_step
                break

            something = framesMap[target_w, target_h]
            if something == 1:
                feedback_snake[6] = step/max_step
                break

            elif something == 2:
                feedback_apple[6] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[6] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(target_w, target_h)
                
        # bottomright
        for step in range(1, self.display_size):
            target_w = snake_head_w + step 
            target_h = snake_head_h + step 

            if(target_w == self.display_size or target_h == self.display_size): 
                feedback_wall[7] = step/max_step
                break

            something = framesMap[target_w, target_h]
            if something == 1:
                feedback_snake[7] = step/max_step
                break

            elif something == 2:
                feedback_apple[7] = step/max_step
                break
            
            elif something == 3:
                feedback_rock[7] = step/max_step
                break
            
            else:
                self.gameGUI.drawSensor(target_w, target_h)
                
        self.gameGUI.update()

        return feedback_apple, feedback_snake, feedback_rock, feedback_wall