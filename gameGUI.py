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
        self.ground_color = (193, 255, 193)
        self.apple_color = (255, 0, 0)
        self.snake_color = (0, 139, 0)
        self.sensor_color = (135, 206, 255)

    def drawFrame(self, frame):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                frame.crashed = True

        pygame.draw.rect(self.display, self.ground_color, pygame.Rect(0, 0, self.size, self.size))
        self.drawGrid()
        
        for position in frame.snake_position:
            pygame.draw.rect(self.display, self.snake_color, pygame.Rect(position[0]*10, position[1]*10, 10, 10))
        
        pygame.draw.rect(self.display, self.apple_color, pygame.Rect(frame.apple_position[0]*10, frame.apple_position[1]*10, 10, 10))
        pygame.display.set_caption('Snake Game - Genetic Algorithm - Score: '+ str(frame.score))
        
    def drawGrid(self):
        blockSize = 10
        for x in range(0, self.size, blockSize):
            for y in range(0, self.size, blockSize):
                pygame.draw.rect(self.display, (200, 200, 200), pygame.Rect(x, y, blockSize, blockSize), 1)
                
    def drawSensor(self, x , y):
        pygame.draw.rect(self.display, self.sensor_color, pygame.Rect(x*10+2, y*10+2, 6, 6))
        
    def update(self):
        pygame.display.update()