'''
Created on Jan 23, 2012

@author: Matej
'''
import pygame
import menu
import random

size=[800,600]
cellSize = 20
grid = (39,29)
print ("Grid size:", grid[0],", " ,grid[1])
speed = 20

BLUE = (0,0,255)
GREEN=(0,255,0)
RED = (255,0,0)

DIRECTIONS = {}
DIRECTIONS["UP"]=(0,-20)
DIRECTIONS["DOWN"]=(0,20)
DIRECTIONS["LEFT"]=(-20,0)
DIRECTIONS["RIGHT"]=(20,0)

COLORS = {1:RED,2:GREEN,3:BLUE,4:(160,160,160),5:(200,200,200)}

pygame.init()

fontSmall = pygame.font.Font("freesansbold.ttf", 16)
fontBig = pygame.font.Font("freesansbold.ttf", 22)

screen=pygame.display.set_mode(size)
isGameOver = False
clock =  pygame.time.Clock()
add = False
count = 0
direction = None 
font = pygame.font.Font("freesansbold.ttf", 16)
snake = []

def findEmptyLocation(grid, snakes):
    ocupied = [snake.sprites for snake in snakes]
    number = grid[0]*grid[1]
    while(True):
        rand = random.randrange(1,number-grid[0])
        if(rand not in ocupied):
            x = (rand / grid[1])
            y = ((rand - x*grid[1]))
            #print ("Food at:",x,", ",y)
            return (x*cellSize,y*cellSize)

def isDirectionOposite(dir1,dir2):
    if(dir1[0]==-dir2[0] and dir1[1]==-dir2[1]): return True
    return False


class FoodManager:
    def __init__(self):
        self.list = []
        self.new()
    def draw(self, screen):
        for food in self.list:
            food.draw(screen)

    def update(self):
        for food in self.list:
            food.timer=food.timer-1
            if food.timer==0:
                self.list.remove(food)
    def new(self):
        rand = random.randrange(1,5)
        food =Food((findEmptyLocation(grid,snake)), COLORS[rand], rand)
        self.list.append(food)
        
class Food:
    def __init__(self,position,color=(150,150,150),value=3, timeToLive=50):
        self.position=position
        self.timer = timeToLive
        self.color=color
        self.value=value
    def draw(self,sreen):
        pygame.draw.rect(screen,self.color,(self.position[0],self.position[1],20,20))

class Sprite:
    def __init__(self, position):
        self.position = position
        self.direction=(0,speed)
    def draw(self,screen,color):
        pygame.draw.rect(screen,color, (self.position[0],self.position[1],cellSize ,cellSize))
    def move(self):
        self.position = (self.position[0]+self.direction[0],self.position[1]+self.direction[1])
        if (self.position[0]/20) < 0: self.position = (grid[0]*20,self.position[1])
        elif self.position[0]/20 > grid[0]: self.position=(0,self.position[1])
        elif (self.position[1]/20<0): self.position=(self.position[0],grid[1]*20)
        elif self.position[1]/20>grid[1]: self.position=(self.position[0], 0)

        
class Snake:
    def __init__(self, position, color):
        self.position=position
        self.color=color
        self.sprites=[]
        self.sprites.append(Sprite(position))
        self.ocupied=[self.position]
        self.crash = False
        self.numToAdd=0
    def move(self):
        directionParent = self.sprites[0].direction
        ocupiedNew = []
        for sprite in self.sprites:
            sprite.move()
            tmp = sprite.direction
            sprite.direction=directionParent
            directionParent = tmp
            ocupiedNew.append(sprite.position)
                

        self.position=self.sprites[0].position
        if(self.position in self.ocupied):
            self.crash=True
        self.ocupied=ocupiedNew
        
        if(self.numToAdd>0):
            self.add(self.numToAdd)
        
    def setDirection(self, direction):
        if(not isDirectionOposite(direction, self.sprites[0].direction)): 
            self.sprites[0].direction=direction
    def draw(self, screen):
        for sprite in self.sprites:
            sprite.draw(screen, self.color)
    def add(self, numToAdd=1):
        position=(0,0)
        last = self.sprites[-1]
        if(last.direction==DIRECTIONS["RIGHT"]): position=(last.position[0]-20,last.position[1])
        elif(last.direction==DIRECTIONS["LEFT"]): position=(last.position[0]+20,last.position[1])
        elif(last.direction==DIRECTIONS["DOWN"]): position=(last.position[0],last.position[1]-20)
        elif(last.direction==DIRECTIONS["UP"]): position=(last.position[0],last.position[1]+20)
        new = Sprite(position)
        new.direction = self.sprites[-1].direction
        self.sprites.append(new)
        self.numToAdd=numToAdd-1
        
        
    
    
food = FoodManager()
#menu = menu.Menu(["Start","Exit"],(200,400),fontSmall,fontBig)
mode = 1

isStarted=False
while(not isStarted):
    event = pygame.event.get()
    for e in event:
        if e.type == pygame.QUIT:
            isGameOver=True
            isStarted=True
            
            
        if e.type==pygame.KEYDOWN:
            key = e.key
            if key == pygame.K_1:
                mode=1
                isStarted=True
            elif key == pygame.K_2:
                mode=2
                isStarted=True
    
    screen.fill((255,255,255))
    msg="Pres 1 for single-player game"
    msgSurface = font.render(msg,False, (20,50,100))
    msgRect = msgSurface.get_rect()
    msgRect.topleft=(300,300)
    
    screen.blit(msgSurface,msgRect)
    
    msg="Pres 2 for two-player game"
    msgSurface = font.render(msg,False, (20,50,100))
    msgRect = msgSurface.get_rect()
    msgRect.topleft=(300,350)
    
    screen.blit(msgSurface,msgRect)
    
    pygame.display.update()
    clock.tick(15)
    



for i in range(0, mode):
    snake.append(Snake(findEmptyLocation(grid, snake),(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))))
while not isGameOver:
    
    rand = random.randrange(0,20)
    if(rand == 3):
        food.new()
    
    screen.fill((255,255,255))
    pygame.draw.rect(screen,(200,200,200),(0*20,0*20,20,20))
    pygame.draw.rect(screen,(200,200,200),(0*20,29*20,20,20))
    pygame.draw.rect(screen,(200,200,200),(39*20,29*20,20,20))
    pygame.draw.rect(screen,(200,200,200),(39*20,0*20,20,20))
    event = pygame.event.get()
    for e in event:
        if e.type == pygame.QUIT:
            isGameOver=True
            
        if e.type==pygame.KEYDOWN:
            key = e.key
            if key == pygame.K_UP:
                snake[0].setDirection(DIRECTIONS["UP"])
            elif key == pygame.K_DOWN:
                snake[0].setDirection(DIRECTIONS["DOWN"])
            elif key == pygame.K_LEFT:
                snake[0].setDirection(DIRECTIONS["LEFT"])
            elif key == pygame.K_RIGHT:
                snake[0].setDirection(DIRECTIONS["RIGHT"])
            elif(mode==2):
                if key == pygame.K_w:
                    snake[1].setDirection(DIRECTIONS["UP"])
                elif key == pygame.K_s:
                    snake[1].setDirection(DIRECTIONS["DOWN"])
                elif key == pygame.K_a:
                    snake[1].setDirection(DIRECTIONS["LEFT"])
                elif key == pygame.K_d:
                    snake[1].setDirection(DIRECTIONS["RIGHT"])
        

        
        
    for s in snake:
        s.move()
    for f in food.list:
        for s in snake:
            if(s.position==f.position):
                s.add(f.value)
                print ("Food: ",f.value)
                food.list.remove(f)
                
            if(s.crash==True):
                isGameOver=True
                print "Snake crash"
    for s in snake:
        s.draw(screen)
    food.draw(screen)
    
    for i,s in enumerate(snake):
        msg = "Score" +str(i+1)+": " + str(len(s.sprites)*10)
        msgSurface = font.render(msg,False, (20,50,100))
        msgRect = msgSurface.get_rect()
        msgRect.topleft=(0 ,i*10)
        
        screen.blit(msgSurface,msgRect)
    
    #menu.draw(screen)
    
    food.update()
    
    pygame.display.update()
    clock.tick(15)
pygame.quit()


    