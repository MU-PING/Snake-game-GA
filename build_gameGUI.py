import pygame, sys

class GameGUI():
    
    def __init__(self, train_or_test, size, framerate=None):
        #initialize pygame modules   
        pygame.init() 
        pygame.display.set_caption(train_or_test + 'SnakeAI Game')
        
        # initialize Clock
        self.clock= pygame.time.Clock() 
        self.framerate = framerate
    
        # display game window
        self.unit = 20
        self.size = size * self.unit
        
        # display info window
        self.height = 4 * self.unit
        
        # display sensor window
        self.width = 18 * self.unit

        # create the display surface object of specific dimension.
        self.display = pygame.display.set_mode((self.size+self.width, self.size+self.height))
        
        # font
        self.copyrightText = pygame.font.Font('Font/font.ttf', 12)
        self.infoText = pygame.font.Font('Font/font.ttf', 14)
        
        # text and position
        self.Gen_y = 8 + self.size
        self.SnakeNo_y = 33 + self.size
        self.Apple_y = 58 + self.size
        self.Gen_TextSurf = self.infoText.render("Generation: Undefined", True, (0, 0, 0))
        self.SnakeNo_TextSurf = self.infoText.render("Snake No.: Best Snake", True, (0, 0, 0))
        self.Apple_TextSurf = None
        
        self.apple_x = 70 + self.size
        self.snake_x = 170 + self.size
        self.wall_x = 270 + self.size
        self.Apple_TextSurf = self.copyrightText.render("Apple", True, (0, 0, 0))
        self.Snake_TextSurf = self.copyrightText.render("Snake", True, (0, 0, 0))
        self.Wall_TextSurf = self.copyrightText.render("Wall", True, (0, 0, 0))
        
        self.direction = 8
        self.direction_x = 10 + self.size
        self.direction_y = [40, 100, 160, 220, 280, 340, 400, 460]
        self.direction_TextSurf = [self.copyrightText.render("T", True, (0, 0, 0)), 
                                   self.copyrightText.render("B", True, (0, 0, 0)),
                                   self.copyrightText.render("L", True, (0, 0, 0)),
                                   self.copyrightText.render("R", True, (0, 0, 0)), 
                                   self.copyrightText.render("TL", True, (0, 0, 0)),
                                   self.copyrightText.render("TR", True, (0, 0, 0)), 
                                   self.copyrightText.render("BL", True, (0, 0, 0)), 
                                   self.copyrightText.render("BR", True, (0, 0, 0))]
        
        self.CopyRight_y = 65 + self.size
        self.CopyRight_TextSurf = self.copyrightText.render("© 2023 Mu-Ping", True, (0, 0, 0))
       
        # color
        self.ground_color = (193, 255, 193)
        self.apple_color = (255, 0, 0)
        self.snake_head_color = (0, 139, 0)
        self.snake_color = (60, 179, 113)
        self.grid_color = (200, 200, 200)
        self.info_color = (255, 229, 180)
        self.sensor_color = (245, 245, 245)

    def drawFrame(self, frames):
        
        if self.framerate:
            self.clock.tick(self.framerate)
            
        # check event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()          

        self.drawBackground()
        self.drawGrid()
        self.drawSnake(frames.snake_position)
        self.drawApple(frames.apple_position)
        self.drawInfo(frames.score)
        self.drawSensor(frames.feedback_apple, frames.feedback_snake, frames.feedback_wall)
    
        pygame.display.update()
        
    def drawBackground(self):
        pygame.draw.rect(self.display, self.ground_color, pygame.Rect(0, 0, self.size, self.size))
        
    def drawGrid(self):
        for x in range(0, self.size, self.unit):
            for y in range(0, self.size, self.unit):
                pygame.draw.rect(self.display, self.grid_color, pygame.Rect(x, y, self.unit, self.unit), 1)
    
    def drawInfo(self, score):
        pygame.draw.rect(self.display, self.info_color, pygame.Rect(0, self.size, self.size, self.height))
        Apple_TextSurf = self.infoText.render("Score: "+str(score), True, (0, 0, 0))
        
        # render
        self.display.blit(self.Gen_TextSurf, (10, self.Gen_y))
        self.display.blit(self.SnakeNo_TextSurf, (10, self.SnakeNo_y))
        self.display.blit(Apple_TextSurf, (10, self.Apple_y))
        self.display.blit(self.CopyRight_TextSurf, (245, self.CopyRight_y))
        
    def drawSensor(self, apples, snakes, walls):
        pygame.draw.rect(self.display, self.sensor_color, pygame.Rect(self.size, 0, self.width, self.size+self.height))
        
        # render title
        self.display.blit(self.Apple_TextSurf, (self.apple_x, 8))
        self.display.blit(self.Snake_TextSurf, (self.snake_x, 8))
        self.display.blit(self.Wall_TextSurf, (self.wall_x, 8))
        
        # render direction
        for i in range(self.direction):
            self.display.blit(self.direction_TextSurf[i], (self.direction_x, self.direction_y[i]))
        
        # render apples, snakes, walls
        for i in range(self.direction):
            apple = self.infoText.render(str(round(apples[i], 3)), True, (0, 0, 0))
            self.display.blit(apple, (self.apple_x, self.direction_y[i]))
        
        for i in range(self.direction):
            snake = self.infoText.render(str(round(snakes[i], 3)), True, (0, 0, 0))
            self.display.blit(snake, (self.snake_x, self.direction_y[i]))
            
        for i in range(self.direction):
            wall = self.infoText.render(str(round(walls[i], 3)), True, (0, 0, 0))
            self.display.blit(wall, (self.wall_x, self.direction_y[i]))
                
        
    def drawSnake(self, snake_position):
        pygame.draw.rect(self.display, self.snake_head_color, pygame.Rect(snake_position[0][0]*self.unit+2, snake_position[0][1]*self.unit+2, 16, 16))
        for position in snake_position[1:]:
            pygame.draw.rect(self.display, self.snake_color, pygame.Rect(position[0]*self.unit+2, position[1]*self.unit+2, 16, 16))
    
    def drawApple(self, apple_position):
        pygame.draw.rect(self.display, self.apple_color, pygame.Rect(apple_position[0]*self.unit+2, apple_position[1]*self.unit+2, 16, 16))
    
    def drawFinalText(self, avg_score):
        finalText = pygame.font.Font('Font/font.ttf', 38) 
        final_TextSurf = finalText.render("Game Over", True, (0, 0, 0))
        final_TextRect = final_TextSurf.get_rect()
        final_TextRect.center = ((self.size/2), (self.size/2))
        self.display.blit(final_TextSurf, final_TextRect)
        
        finalScore = pygame.font.Font('Font/font.ttf', 18) 
        final_ScoreSurf = finalScore.render("Average Score: "+str(avg_score), True, (0, 0, 0))
        final_ScoreRect = final_ScoreSurf.get_rect()
        final_ScoreRect.center = ((self.size/2), (self.size/2)+50)
        self.display.blit(final_ScoreSurf, final_ScoreRect)
        
        pygame.display.update()
        
    def setGen(self, gen):
        self.Gen_TextSurf = self.infoText.render("Generation: "+gen, True, (0, 0, 0))
        
    def setSnakeNO(self, snakeNO):
        self.SnakeNo_TextSurf = self.infoText.render("Snake No.: "+snakeNO, True, (0, 0, 0))    
    
    def maintain(self):
        while 1 :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                    
    
    def quitGUI(self):
        pygame.quit()  
    

        