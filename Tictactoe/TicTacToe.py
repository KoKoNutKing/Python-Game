import pygame

pygame.init()

class squ():
    def __init__(self,x,y,ans,ticked):
        self.x =x
        self.y =y
        self.ans =ans
        self.ticked = ticked
        ob.append(self)
    def create(self):
        global turn,win
        font = pygame.font.Font('freesansbold.ttf', 72)
        font_win = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render(self.ans, True, "Red")
        text_win = font_win.render('',True,"red")

        if win:
            text_win = font_win.render(f'Player {turn} won',True,"red")
        elif turns > 9:
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
        

    def click(self):
        global turn,turns,GameOver
        self.checkx = self.x < x_mo < (self.x+squ_size)
        self.checky = self.y < y_mo < (self.y+squ_size)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.checkx and self.checky and not self.ticked and not GameOver:
                if turn == "O":
                    self.ans = "X"
                    turn = "X"
                elif turn == "X":
                    self.ans = "O"
                    turn = "O"
                self.ticked = True
                turns +=1
                print(turn,turns)
                
def win_lose():
    global GameOver,win
    board = [[squ00.ans,squ01.ans,squ02.ans],[squ10.ans,squ11.ans,squ12.ans],[squ20.ans,squ21.ans,squ22.ans]]
    # print(board)
    if (board[0][0] == board[0][1] == board[0][2])\
        or (board[1][0] == board[1][1] == board[1][2])\
        or (board[2][0] == board[2][1] == board[2][2])\
        or (board[0][0] == board[1][0] == board[2][0])\
        or (board[0][1] == board[1][1] == board[2][1])\
        or (board[0][2] == board[1][2] == board[2][2])\
        or (board[0][0] == board[1][1] == board[2][2])\
        or (board[0][2] == board[1][1] == board[2][0]):
            GameOver = True
            win = True
    elif turns > 9:
        GameOver = True


                
x_Scr = 1370
y_Scr = 725


Scr = pygame.display.set_mode((x_Scr,y_Scr),pygame.RESIZABLE)
running = True

ob = []
turn = "X"
turns = 1
GameOver = False
win = False


x_cen = x_Scr/2
y_cen = y_Scr/2
squ_size = 150
squ_dis = squ_size/6



squ11 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2,"11",False)
squ01 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2-(squ_dis+squ_size),"01",False)
squ21 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2+(squ_dis+squ_size),"21",False)

squ00 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"00",False)
squ10 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2,"10",False)
squ20 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"20",False)

squ02 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"02",False)
squ12 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2,"12",False)
squ22 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"22",False)


        

while running:
    Scr.fill((32,32,32))
    x_mo,y_mo= pygame.mouse.get_pos()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for i in ob:
            i.click()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and GameOver:
                ob.clear()
                squ11 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2,"11",False)
                squ01 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2-(squ_dis+squ_size),"01",False)
                squ21 = squ((x_Scr-squ_size)/2,(y_Scr-squ_size)/2+(squ_dis+squ_size),"21",False)

                squ00 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"00",False)
                squ10 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2,"10",False)
                squ20 = squ((x_Scr-squ_size)/2-(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"20",False)

                squ02 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2-(squ_dis+squ_size),"02",False)
                squ12 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2,"12",False)
                squ22 = squ((x_Scr-squ_size)/2+(squ_dis+squ_size),(y_Scr-squ_size)/2+(squ_dis+squ_size),"22",False)
                turn = "X"
                turns = 1
                win = False
                GameOver = False
    for i in ob:
        i.create()
    win_lose()
    pygame.display.flip()

pygame.quit()