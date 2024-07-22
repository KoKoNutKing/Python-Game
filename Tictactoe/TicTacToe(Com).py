import pygame
import random
import numpy as np

pygame.init()

class squ():
    def __init__(self,x,y,name,ans,ticked):
        self.x =x
        self.y =y
        self.name = name
        self.ans =ans
        self.ticked = ticked
        ob.append(self)
    def __str__(self):
        return self.name
    def create(self):
        global turn,win
        font = pygame.font.Font('freesansbold.ttf', 72)
        font_win = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render(self.ans, True, "Red")
        text_win = font_win.render('',True,"red")

        if win:
            text_win = font_win.render(f'{turn} won',True,"red")
        elif turns > 8:
            text_win = font_win.render('Tie',True,"red")
            
        text_R = font_win.render('press R to play again',True,"red",)
        
        RRect=text_R.get_rect()
        RRect.center = (x_cen,y_cen+squ_size*2)
        textRect = text.get_rect()
        winRect=text_win.get_rect()
        winRect.center = (x_cen,y_cen-squ_size*2)
        textRect.center = (self.x+squ_size/2,self.y+squ_size/2)
    
        pygame.draw.rect(Scr,"white",(self.x,self.y,squ_size,squ_size))

        if self.ans == "X" or self.ans == "O":
            Scr.blit(text,textRect)

        if GameOver:
            Scr.blit(text_win,winRect)
            Scr.blit(text_R,RRect)
        
    def com_cal(self):
        global board,priority,priority1,priority2
        test_x = int(self.name[0])
        test_y = int(self.name[1])

        def make_line(a,lista):
            global board,priority,priority1,priority2
            test_x = int(self.name[0])
            test_y = int(self.name[1])

            for i in [1,0,-1]:
                    for j in [1,0,-1]:
                        x_i = test_x+i
                        y_j = test_y+j
                        if (x_i in [0,1,2])  and (y_j in [0,1,2]) and (board[x_i,y_j].ans == a)and (board[x_i,y_j] != self)\
                            and not (board[x_i,y_j] in lista):
                            
                            if (test_x+(2*i) in [0,1,2]) and (test_y+(2*j) in [0,1,2]) and not board[test_x+2*i,test_y+2*j].ticked:
                                lista.append(board[test_x+2*i,test_y+2*j])
                            if (test_x-i in [0,1,2]) and (test_y-j in [0,1,2]) and not board[test_x-i,test_y-j].ticked:
                                lista.append(board[test_x-i,test_y-j])
        #pri
        
        if self.ans == "X":    

            for i in [1,0,-1]:
                for j in [1,0,-1]:
                    x_i = test_x+i
                    y_j = test_y+j
                    if (x_i in [0,1,2])  and (y_j in [0,1,2]) and not (board[x_i,y_j].ticked) and not (board[x_i,y_j] in priority):
                        priority.append(board[x_i,y_j])

        #1
        if self.ans == "O":
            make_line("O",priority1)
        if self.ans == "X":
            make_line("X",priority2)

        
        
        if self.ticked:
            try:
                priority.remove(self)
                priority1.remove(self)
                priority2.remove(self)
            except:
                pass
                



        

    def Gamerule(self):
        global turn,turns,GameOver,win,com_choice,first,priority,priority1
        self.checkx = self.x < x_mo < (self.x+squ_size)
        self.checky = self.y < y_mo < (self.y+squ_size)
        def choose(x):
            global com_choice
            com_choice = random.choice(x)
            dem = 0
            while com_choice.ticked:
                dem += 1
                com_choice = random.choice(x)
                if dem > 60:
                    dem = 0
                    return 0
                    break
        win_lose()
        
        if turns %2 ==0:
            turn = "Human"
        elif turns %2 ==1:
            turn = "Com"

        if turn == "Com" and not GameOver:
            if priority2 != []:
                choose(priority2)
                if priority1 != [] and choose(priority2) ==0:
                    choose(priority1)
                elif priority != []:
                    choose(priority)
                else:
                    choose(ob)
            elif priority1 != []:
                choose(priority1)
            elif priority != []:
                choose(priority)
            else:
                choose(ob)
            
            com_choice.ticked = True
            com_choice.ans = "X"
            turns +=1
            
        elif turn == "Human" and not GameOver:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.checkx and self.checky and not self.ticked :
                    self.ans = "O"
                    self.ticked = True
                    turns +=1
                    if self in priority2:
                        priority2.remove(self)
                    

        if GameOver and first:
            turns +=1
            first = False
            


                
def win_lose():
    global GameOver,win
    if (board[0,0].ans == board[0,1].ans == board[0,2].ans != '')\
        or (board[1,0].ans == board[1,1].ans == board[1,2].ans != '')\
        or (board[2,0].ans == board[2,1].ans == board[2,2].ans != '')\
        or (board[0,0].ans == board[1,0].ans == board[2,0].ans != '')\
        or (board[0,1].ans == board[1,1].ans == board[2,1].ans != '')\
        or (board[0,2].ans == board[1,2].ans == board[2,2].ans != '')\
        or (board[0,0].ans == board[1,1].ans == board[2,2].ans != '')\
        or (board[0,2].ans == board[1,1].ans == board[2,0].ans != ''):
            GameOver = True
            win = True
    elif turns > 8:
        GameOver = True 
    




                
x_Scr = 1370
y_Scr = 725


Scr = pygame.display.set_mode((x_Scr,y_Scr),pygame.RESIZABLE)
running = True

ob = []
priority1 = []
priority = []
priority2 = []


turn = ''
turns = 0
GameOver = False
win = False
com_choice = ''
first = True




x_cen = x_Scr/2
y_cen = y_Scr/2
squ_size = 150
squ_dis = squ_size/6



squ11 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2,"11",'',False)
squ01 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2-(squ_dis+squ_size),"01",'',False)
squ21 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2+(squ_dis+squ_size),"21",'',False)

squ00 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"00",'',False)
squ10 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2,"10",'',False)
squ20 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"20",'',False)

squ02 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"02",'',False)
squ12 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2,"12",'',False)
squ22 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"22",'',False)

board = np.array([[squ00,squ01,squ02],[squ10,squ11,squ12],[squ20,squ21,squ22]])



        

while running:
    Scr.fill((32,32,32))
    x_mo,y_mo= pygame.mouse.get_pos()

    for i in ob:
        i.create()
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for i in ob:
            i.Gamerule()
            i.com_cal()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and GameOver:
                for i in ob:
                    del i
                ob.clear()
                priority.clear()
                priority1.clear()
                priority2.clear()

                squ11 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2,"11",'',False)
                squ01 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2-(squ_dis+squ_size),"01",'',False)
                squ21 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2+(squ_dis+squ_size),"21",'',False)

                squ00 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"00",'',False)
                squ10 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2,"10",'',False)
                squ20 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"20",'',False)

                squ02 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"02",'',False)
                squ12 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2,"12",'',False)
                squ22 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"22",'',False)
                board = np.array([[squ00,squ01,squ02],[squ10,squ11,squ12],[squ20,squ21,squ22]])


                
                turn = ''
                turns = 0
                GameOver = False
                win = False
                com_choice = ''
                first = True

    pygame.display.flip()

pygame.quit()