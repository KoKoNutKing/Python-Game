import pygame
import sys, os
from time import sleep

current_dir = os.path.dirname(__file__)
healpool = 100
damage = 10

pygame.init()
Screen = pygame.display.set_mode((1370,725),pygame.RESIZABLE)
pygame.display.set_caption('Just A 2 Players Game')

color0 = "saddle brown"
color1 = (32,32,32)
GameOver = False
running = True
x_Scr, y_Scr = Screen.get_size()



class pl():
    Losing = ""
    speed = 2
    def __init__(self,name,x,y,pic,jumping,jtime,hp,color):
        self.x = x
        self.y = y
        self.jumping = jumping
        self.jtime = jtime
        self.hp = hp
        self.x0 = x
        self.y0 =y
        self.view = ""
        self.name = name
        self.pic = pic
        self.pic_pos = True
        self.ptime = 0
        self.color = color
        

    def gamerule(self):
        #Gravity
        if self.y < y0 :
            self.y += (self.y-200)*0.015
        if self.y > y0:
            self.y = y0
            self.jtime = 0

        if (self.jumping) and (self.jtime <= 30):
            self.y -= (self.y-100)*0.025
            self.jtime += 1 
        
        #Health pool
        if self.hp <= 0:
            pl.Losing = self.name
        
        #pic's View
        if self.view == "r" and self.pic_pos == True:
            self.pic = os.path.join(current_dir, os.path.join(current_dir, "pl.png"))
        elif self.view == "l" and self.pic_pos == True:
            self.pic = os.path.join(current_dir, os.path.join(current_dir, "pl[R].png"))

        if self.pic_pos == False:
            self.ptime += 1
            if self.ptime == 60:
                self.pic_pos = True
                self.ptime = 0

    def create(self):
        # pygame.draw.rect(Screen, self.color,(self.x ,self.y ,20,20))
        Screen.blit(pygame.image.load(self.pic).convert(), (self.x,self.y))

        font = pygame.font.Font("freesansbold.ttf", 28)
        text = font.render(str(self.hp), True, "red")
        text_name = font.render(self.name, True, self.color)
        textRect = text.get_rect()
        textRect_name = text_name.get_rect()

        textRect.center = (self.x0, self.y0-400)
        textRect_name.center = (self.x, self.y-40)
        
        Screen.blit(text, textRect) 
        Screen.blit(text_name,textRect_name) 
    

class bullet():
    def __init__(self,x,y,speed, dmg,belong):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.speed = speed
        self.belong = belong
    
    def create(self):
        pygame.draw.rect(Screen, "yellow",(self.x ,self.y ,4,4))
        self.x += self.speed
        if self.x >= 1370:
            obs.remove(self)
        if (pl2.x < (self.x+4) < (pl2.x+20)) and (pl2.y<(self.y+4) < (pl2.y+20)) and (self.belong=="pl1"):
            pl2.hp -= self.dmg
            obs.remove(self)
        if (pl1.x < (self.x+4) < (pl1.x+20)) and (pl1.y<(self.y+4) < (pl1.y+20)) and (self.belong=="pl2"):
            pl1.hp -= self.dmg
            obs.remove(self)
        if GameOver:
            self.speed =0

def result():
    font = pygame.font.Font("freesansbold.ttf", 32)
    if pl.Losing == "pl1":
        text = font.render("PLayer 2 won", True, "red")
        textRect = text.get_rect()

        textRect.center = (x_Scr/2, y_Scr/2-200)
        Screen.blit(text, textRect) 
    elif pl.Losing == "pl2":
        text = font.render("Player 1 won", True, "red")
        textRect = text.get_rect()

        textRect.center = (x_Scr/2, y_Scr/2-200)
        Screen.blit(text, textRect) 

obs=[]



pl1 = pl("pl1",300,455,os.path.join(current_dir, os.path.join(current_dir, "pl.png")),False,0, 100,"orange")
pl2 = pl("pl2",1370-pl1.x,455,os.path.join(current_dir, os.path.join(current_dir, "pl[R].png")),False,0, 100,"cyan")
x0 = 0
y0 =455

while running:
    Screen.fill(color1)

    land = pygame.draw.rect(Screen,color0 ,(x0,y0+20,1370,725-y0))

    pl1.create()
    pl2.create()
    
    for i in obs:
        i.create()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and (not GameOver):
            if event.key == pygame.K_w and (pl1.y >= y0) :
                pl1.jumping =True
                
            if event.key == pygame.K_UP and (pl2.y >= y0) :
                pl2.jumping =True  

            if (event.key == pygame.K_f) and (pl1.view == "r"):
                ob1= bullet(pl1.x+16,pl1.y+8,4,damage,"pl1")
                pl1.pic = os.path.join(current_dir, os.path.join(current_dir, "shooting.png"))
                pl1.pic_pos = False
                obs.append(ob1) 
            elif (event.key == pygame.K_f) and (pl1.view == "l"):
                ob1= bullet(pl1.x,pl1.y+8,-4,damage, "pl1")
                pl1.pic = os.path.join(current_dir, os.path.join(current_dir, "shooting[R].png"))
                pl1.pic_pos = False
                obs.append(ob1) 

            if (event.key == pygame.K_KP_1) and (pl2.view =="l"):
                ob1= bullet(pl2.x,pl2.y+8,-4,damage, "pl2")
                pl2.pic = os.path.join(current_dir, os.path.join(current_dir, "shooting[R].png"))
                pl2.pic_pos = False
                obs.append(ob1) 
            elif (event.key == pygame.K_KP_1) and (pl2.view =="r"):
                ob1= bullet(pl2.x+16,pl2.y+8,4,damage,"pl2")
                pl2.pic = os.path.join(current_dir, os.path.join(current_dir, "shooting.png"))
                pl2.pic_pos = False
                obs.append(ob1) 
        
        if event.type == pygame.KEYDOWN and (GameOver): 
            if event.key == pygame.K_r: 
                pl1 = pl("pl1",300,455,os.path.join(current_dir, os.path.join(current_dir, "pl.png")),False,0, healpool,"orange")
                pl2 = pl("pl2",1370-pl1.x,455,os.path.join(current_dir, os.path.join(current_dir, "pl[R].png")),False,0, healpool,"cyan")       
                pl.Losing =""
                obs.clear()
                GameOver = False
        
        if pl1.x+10 < pl2.x+10:
            pl1.view = "r"
            pl2.view = "l"
        elif pl1.x+10 >= pl2.x+10:
            pl2.view = "r"
            pl1.view = "l"


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w :
                pl1.jumping = False
                pl1.jtime = 0
            
            if event.key == pygame.K_UP:
                pl2.jumping = False
                pl2.jtime = 0
        

    if not GameOver:
        keys = pygame.key.get_pressed()
        pl1.x += (keys[pygame.K_d] - keys[pygame.K_a]) *pl.speed
        pl2.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])*pl.speed
            
        pl1.gamerule()
        pl2.gamerule()        
    result()
    if pl.Losing != "":
        GameOver=True
        

    pygame.display.flip()

pygame.quit()
sys.exit()