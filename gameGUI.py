import pygame
import random
import sys

class GameGUI():
    def __init__(self, size):

        #initialize pygame modules   
        pygame.init() 
        
        # initialize Clock
        self.clock= pygame.time.Clock() 
        
        # display game window
        self.size = size*10

        # create the display surface object of specific dimension.
        self.display = pygame.display.set_mode((self.size, self.size))
        
        # color
        self.ground_color = (247, 255, 224)
        self.apple_color = (255, 0, 0)
        self.snake_color = (62, 49, 41)

    def update(self, frame):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                frame.crashed = True

        pygame.draw.rect(self.display, self.ground_color, pygame.Rect(0, 0, self.size, self.size))
        
        for position in frame.snake_position:
            pygame.draw.rect(self.display, self.snake_color, pygame.Rect(position[0]*10, position[1]*10, 10, 10))
        
        pygame.draw.rect(self.display, self.apple_color, pygame.Rect(frame.apple_position[0]*10, frame.apple_position[1]*10, 10, 10))
        pygame.display.set_caption('Snake Game - Genetic Algorithm - Score: '+ str(frame.score))
        pygame.display.update()
