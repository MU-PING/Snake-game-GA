import pygame, sys

class GameGUI():
    
    def __init__(self, train_or_test, size):
        #initialize pygame modules   
        pygame.init() 
        pygame.display.set_caption(train_or_test + 'SnakeAI Game')
        
        # initialize Clock
        self.clock= pygame.time.Clock() 
        
        # display game window
        self.unit = 20
        self.size = size * self.unit
        
        # display info window
        self.height = 4 * self.unit

        # create the display surface object of specific dimension.
        self.display = pygame.display.set_mode((self.size, self.size+self.height))
        
        # font
        self.copyrightText = pygame.font.Font('font.ttf', 12)
        self.infoText = pygame.font.Font('font.ttf', 14)
        self.finalText = pygame.font.Font('font.ttf', 38)
        self.Gen_TextSurf = self.infoText.render("Generation: Undefined", True, (0, 0, 0))
        self.Snake_TextSurf = self.infoText.render("Snake No.: Undefined", True, (0, 0, 0))
        self.Score_TextSurf = self.infoText.render("Score: Undefined", True, (0, 0, 0))
        self.CopyRight_TextSurf = self.copyrightText.render("© 2023 Mu-Ping", True, (0, 0, 0))
        self.final_TextSurf = self.finalText.render("Game Over", True, (0, 0, 0))
        self.final_TextRect = self.final_TextSurf.get_rect()
        self.final_TextRect.center = ((self.size/2),(self.size/2))
       
        # color
        self.ground_color = (193, 255, 193)
        self.apple_color = (255, 0, 0)
        self.snake_head_color = (0, 139, 0)
        self.snake_color = (60, 179, 113)

    def drawFrame(self, frames):
        
        # check event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                frames.crashed = True

        self.drawBackground()
        self.drawGrid()
        self.drawInfo(frames.apple)
        self.drawSnake(frames.snake_position)
        self.drawApple(frames.apple_position)
        
        pygame.display.update()
        
    def drawBackground(self):
        pygame.draw.rect(self.display, self.ground_color, pygame.Rect(0, 0, self.size, self.size))
        
    def drawGrid(self):
        for x in range(0, self.size, self.unit):
            for y in range(0, self.size, self.unit):
                pygame.draw.rect(self.display, (200, 200, 200), pygame.Rect(x, y, self.unit, self.unit), 1)
    
    def drawInfo(self, score):
        pygame.draw.rect(self.display, (255, 229, 180), pygame.Rect(0, self.size, self.size, self.height))
        self.Score_TextSurf = self.infoText.render("Score: "+str(score), True, (0, 0, 0))
        
        # render
        self.display.blit(self.Gen_TextSurf, (10, 8+self.size))
        self.display.blit(self.Snake_TextSurf, (10, 33+self.size))
        self.display.blit(self.Score_TextSurf, (10, 58+self.size))
        self.display.blit(self.CopyRight_TextSurf, (245, 65+self.size))
    
    def drawSnake(self, snake_position):
        pygame.draw.rect(self.display, self.snake_head_color, pygame.Rect(snake_position[0][0]*self.unit+2, snake_position[0][1]*self.unit+2, 16, 16))
        for position in snake_position[1:]:
            pygame.draw.rect(self.display, self.snake_color, pygame.Rect(position[0]*self.unit+2, position[1]*self.unit+2, 16, 16))
    
    def drawApple(self, apple_position):
        pygame.draw.rect(self.display, self.apple_color, pygame.Rect(apple_position[0]*self.unit+2, apple_position[1]*self.unit+2, 16, 16))
    
    def drawFinalText(self):
        self.display.blit(self.final_TextSurf, self.final_TextRect)
    
    def setGen(self, gen):
        self.Gen_TextSurf = self.infoText.render("Generation: "+str(gen), True, (0, 0, 0))
        
    def setSnakeNO(self, snakeNO):
        self.Snake_TextSurf = self.infoText.render("Snake No.: "+str(snakeNO), True, (0, 0, 0))    
    
    def loopGUI(self, score):
        while 1 :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                    
            self.drawBackground()
            self.drawGrid()
            self.drawFinalText()
            self.drawInfo(score)
            
            pygame.display.update()
            
    def quitGUI(self):
        pygame.quit()  
    

        