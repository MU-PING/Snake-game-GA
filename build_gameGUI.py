import pygame

class GameGUI():
    
    def __init__(self, size):
        #initialize pygame modules   
        pygame.init() 
        
        # initialize Clock
        self.clock= pygame.time.Clock() 
        
        # display game window
        self.unit = 20
        self.size = size * self.unit

        # create the display surface object of specific dimension.
        self.display = pygame.display.set_mode((self.size, self.size))
        
        # color
        self.ground_color = (193, 255, 193)
        self.apple_color = (255, 0, 0)
        self.snake_head_color = (0, 139, 0)
        self.snake_color = (60, 179, 113)
        self.sensor_color = (173, 173, 173)
        self.sensor_apple_color = (102, 102, 102)

    def drawFrame(self, frames, training):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                frames.crashed = True

        pygame.draw.rect(self.display, self.ground_color, pygame.Rect(0, 0, self.size, self.size))
        self.drawGrid()
        
        # draw snake
        pygame.draw.rect(self.display, self.snake_head_color, pygame.Rect(frames.snake_position[0][0]*self.unit+1, frames.snake_position[0][1]*self.unit+1, 18, 18))
        for position in frames.snake_position[1:]:
            pygame.draw.rect(self.display, self.snake_color, pygame.Rect(position[0]*self.unit+1, position[1]*self.unit+1, 18, 18))
        
        # draw apple
        pygame.draw.rect(self.display, self.apple_color, pygame.Rect(frames.apple_position[0]*self.unit+1, frames.apple_position[1]*self.unit+1, 18, 18))
        
        # draw caption
        if training:
            train_or_test = "Training"
        else:
            train_or_test = "Testing Best"
            
        pygame.display.set_caption(train_or_test +' Apple: '+ str(frames.apple))
        pygame.display.update()
        
    def drawGrid(self):
        for x in range(0, self.size, self.unit):
            for y in range(0, self.size, self.unit):
                pygame.draw.rect(self.display, (200, 200, 200), pygame.Rect(x, y, self.unit, self.unit), 1)
        
    def quitGUI(self):
        pygame.quit()    