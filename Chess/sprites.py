import pygame
from config import *

play='W'
all_sprites = pygame.sprite.LayeredUpdates()
class Board:
    def __init__(self):
        self.board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'], 
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                      [0, 0, 0, 0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0, 0, 0, 0], 
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                      ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        
        self.create_board()
        
        #number

    def draw_squares(self,screen):
        screen.fill(DARK)
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(screen, LIGHT, (row*TITLESIZE,col*TITLESIZE, TITLESIZE, TITLESIZE))


    def move(self, piece, row, col):
        if piece.type == 'K':
            if piece.row == row and piece.col-col ==2 and not self.board[piece.row][piece.col-4] != 0:
                self.board[piece.row][piece.col-4].move(row,col+1)
                self.board[piece.row][piece.col-4],self.board[row][col+1] = self.board[row][col+1],self.board[piece.row][piece.col-4]
                
                self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
                piece.move(row,col)
            elif piece.row == row and -piece.col+col ==2 and not self.board[piece.row][piece.col+3] != 0:
                self.board[piece.row][piece.col+3].move(row,col-1)
                self.board[piece.row][piece.col+3],self.board[row][col-1] = self.board[row][col-1],self.board[piece.row][piece.col+3]
                
                self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
                piece.move(row,col)
            else:
                self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
                piece.move(row,col)
        else:
            self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
            piece.move(row,col)
        
    def take(self, piece, row, col):
        self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        self.board[piece.row][piece.col].kill()
        self.board[piece.row][piece.col] =0
        piece.move(row,col)
        

        
        
        
    def get_piece(self,row,col):
        return self.board[row][col]
    
    def check_check(self, turn):
        invalid_moves = []
        K_pos = ()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0 and self.board[i][j].team == turn and self.board[i][j].type == 'K':
                    K_pos = (i,j)
        for sprite in all_sprites:
            if turn != sprite.team :
                if sprite.type != 'P':
                    invalid_moves += self.get_valid_moves(sprite)
                else:
                    invalid_moves += pawn(sprite, self.board)
                
        if K_pos in invalid_moves:
            return (True,invalid_moves)
        else:
            return (False,invalid_moves)
        
    def check(self, piece, row, col):
        self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        ans = self.check_check(piece.team)[0]
        self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        return ans

    def checkmate(self, turn, check):
        if check:
            for sprite in all_sprites:
                if sprite.team == turn:
                    for move in self.get_valid_moves(sprite):
                        row, col = move
                        if not self.check(sprite, row, col):
                            return False
            return True
        else:
            return False

    def stalemate(self, turn, check):
        if not check and self.check_check(self, turn)[1] == []:
            return True
        else:
            return False

    def castle(self,king):
        s_castle = False
        l_castle = False
        if not king.moved:
            if self.board[king.row][king.col+3] != 0 and not self.board[king.row][king.col+3].moved:
                s_castle = True
            if self.board[king.row][king.col-4] != 0 and not self.board[king.row][king.col-4].moved:
                l_castle = True
        return s_castle, l_castle
    
    def create_board(self):
        for col in range(COLS):
            for row in range(6,8):
                if self.board[row][col] == 0:
                    pass
                else:
                    self.board[row][col] = Piece(row, col, play, self.board[row][col])
        for col in range(COLS):
            for row in range(0,2):
                if self.board[row][col] == 0:
                    pass
                else:
                    self.board[row][col] = Piece(row, col, 'B', self.board[row][col])

    def get_valid_moves(self,piece):
        moves = []
        

        if piece.type == 'K':
            s,l = self.castle(piece)
            print(self.board)
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    x = piece.row+i
                    y = piece.col+j
                    if x in range(8) and y in range(8):
                        if self.board[x][y]==0:
                            moves.append((x,y))
                        elif self.board[x][y].team != piece.team:
                            moves.append((x,y))

            if s and not [i for i in range(1,3) if self.board[piece.row][piece.col+i] != 0]:
                moves.append((piece.row, piece.col+2))
            if l and not [i for i in range(1,4) if self.board[piece.row][piece.col-i] != 0]:
                moves.append((piece.row, piece.col-2))
            

        if piece.type == 'P':
            if piece.team == 'W':
                j = -1
            else:
                j = 1
            if piece.row +j in range(8):
                if self.board[piece.row+j][piece.col] == 0:
                    if piece.row == int(3.5-2.5*j) and self.board[piece.row+2*j][piece.col] == 0 :
                        moves.append((piece.row+2*j,piece.col)) 
                    moves.append((piece.row+j,piece.col))
                for i in [-1,1]:
                    if piece.col+i in range(8):
                        if self.board[piece.row+j][piece.col+i] != 0:
                            if self.board[piece.row+j][piece.col+i].team != piece.team:
                                moves.append((piece.row+j,piece.col+i))

            
        if piece.type == 'Q':
            moves += F(piece, self.board)
            moves += B(piece, self.board)
            moves += R(piece, self.board)
            moves += L(piece, self.board)
            moves += BR(piece, self.board)
            moves += FR(piece, self.board)
            moves += BL(piece, self.board)
            moves += FL(piece, self.board)

        if piece.type == 'R':
            moves += F(piece, self.board)
            moves += B(piece, self.board)
            moves += R(piece, self.board)
            moves += L(piece, self.board)
        if piece.type == 'N':
            for i in [2,-2]:
                for j in [1,-1]:
                    x = piece.row+i
                    y = piece.col+j
                    if x in range(8) and y in range(8):
                        if self.board[x][y] == 0:
                            moves.append((x,y))
                        elif self.board[x][y].team != piece.team:
                            moves.append((x,y))
                    x = piece.row+j
                    y = piece.col+i
                    if x in range(8) and y in range(8):
                        if self.board[x][y] == 0:
                            moves.append((x,y))
                        elif self.board[x][y].team != piece.team:
                            moves.append((x,y))
        if piece.type == 'B':
            moves += BR(piece, self.board)
            moves += FR(piece, self.board)
            moves += BL(piece, self.board)
            moves += FL(piece, self.board)

        return list(set(moves))


class Piece(pygame.sprite.Sprite):
    def __init__(self, row, col, team, type):
        self.row = row
        self.col = col
        self.team = team
        self.type = type
        self.moved = False
        self._layer = 1
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        

        self.img =pygame.transform.scale(pygame.image.load("img\pieces.png").convert(),(4*TITLESIZE,4*TITLESIZE))
        self.Create_img()

        self.x = 0
        self.y = 0
        self.Calculate_pos()
        

        

        #1-26p
    def Calculate_pos(self):
        self.x = self.col*TITLESIZE
        self.y = self.row*TITLESIZE
        self.rect = self.image.get_rect()
        self.rect.x =self.x
        self.rect.y = self.y

    def Create_img(self):
        if self.team == 'W':
            i=0
        if self.team == 'B':
            i=2
        if self.type == 'K':
            j=0
        if self.type == 'Q':
            j=1
        if self.type == 'R':
            j=2
        if self.type == 'N':
            j=3
        if self.type == 'B':
            i+=1
            j=0
        if self.type == 'P':
            i+=1
            j=1
        

        self.image = pygame.Surface([90,90])
        self.image.blit(self.img, (0,0), (j*TITLESIZE,i*TITLESIZE,90,90))
        self.image.set_colorkey("BLACK")

    def move(self,row,col):
        self.row = row
        self.col = col
        self.moved = True
        self.Calculate_pos()

    def __repr__(self):
        return(f'{self.team}{self.type}')


class Game():
    def __init__(self,screen):
        self.font = pygame.font.Font('04B_19.TTF', 40)
        self._init()
        self.screen = screen
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = 'W'
        self.playing = True
        self.check = False
        self.checkmate = False
        self.stalemate = False
        self.won = 'None'
        self.valid_move = []


    def update(self):
        self.board.draw_squares(self.screen)
        self.draw_valid_moves(self.valid_move)
        self.draw_check()
        all_sprites.draw(self.screen)
        self.result()
        self.play_again()
        pygame.display.update() 


    def reset(self):
        self._init()

    def play_again(self):
        if self.playing == False:
            pygame.draw.rect(self.screen, 'BLACk', (95,195, 530,330))
            pygame.draw.rect(self.screen, 'GREY', (100,200, 520,320))
            self.text = self.font.render(self.won, True, 'BLACK')
            self.text_rect= self.text.get_rect(center=(360,300))
            self.screen.blit(self.text, self.text_rect)
            play_again = Button(300,400, 120,60, LIGHT, DARK, 'again',32)
            self.screen.blit(play_again.image, play_again.rect)
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_again.is_press(mouse_pos, mouse_pressed) or keys[pygame.K_r]:
                for sprite in all_sprites:
                    sprite.kill()
                self.reset()
                self.playing == False

            

    def result(self):
        if self.checkmate:
            if self.turn == 'B':
                self.won = 'WHITE'
            else:
                self.won = 'BLACK'
            self.playing = False
            
        elif self.stalemate:
            self.won = 'DRAW'
            self.playing = False

            



    def select(self, row, col):
        if self.playing == True:
            if self.selected:
                result = self._move(self.selected.team,row,col)
                if not result:
                    self.selected = None
                    self.select(row,col)

            else:
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.team == self.turn :
                    self.selected = piece
                    if piece.type == 'K':
                        self.valid_move = [i for i in self.board.get_valid_moves(piece) if i not in self.board.check_check(self.turn)[1]]
                    else:
                        self.valid_move = self.board.get_valid_moves(piece)
                    return True
            return False


    def _move(self, team, row, col):
        piece = self.board.get_piece(row,col)
        if self.selected and (row,col) in self.valid_move and piece == 0:
            if not self.board.check(self.selected, row, col):
                self.board.move(self.selected, row, col)
                self._change_turn()
        elif self.selected and (row,col) in self.valid_move and piece.team != team:
            if not self.board.check(self.selected, row, col):
                self.board.take(self.selected, row, col)
                self._change_turn()
        else:
            return False
        self.valid_move = []
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLUE, ((col+0.5)*TITLESIZE,(row+0.5)*TITLESIZE), 20)
    def draw_check(self):
        for sprite in all_sprites:
            if sprite.type == 'K' and sprite.team == self.turn:
                king = sprite
        if self.check:
            print(king.row, king.col)
            pygame.draw.rect(self.screen, 'RED', (king.col*TITLESIZE+10,king.row*TITLESIZE+10,70,70 ))
    def _change_turn(self):
        

        if self.turn == 'W':
            self.turn = 'B'
        else:
            self.turn = 'W'
        self.selected = None
        self.check = self.board.check_check(self.turn)[0]
        self.checkmate = self.board.checkmate(self.turn, self.check)

class Button():
    def __init__(self, x,y,width,height,fg,bg,content,fontsize):
        self.font = pygame.font.Font('04B_19.TTF',fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg


        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect() 

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect= self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text, self.text_rect)




    def is_press(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

        
        
def F(piece, board):
    moves = []
    for i in range(1,7):
        x = piece.row+i
        
        if x in range(8):
            if board[x][piece.col] == 0:
                moves.append((x,piece.col))
            elif board[x][piece.col].team != piece.team:
                moves.append((x,piece.col))
            if (board[x][piece.col] != 0):
                break     
    return moves
def B(piece, board):
    moves = []
    for i in range(1,7):
        x = piece.row-i
        
        if x in range(8):
            if board[x][piece.col] == 0:
                moves.append((x,piece.col))
            elif board[x][piece.col].team != piece.team:
                moves.append((x,piece.col))
            if (board[x][piece.col] != 0):
                break      
    return moves
def L(piece, board):
    moves = []
    for i in range(1,7):
        y = piece.col-i
        
        if y in range(8):
            if board[piece.row][y] == 0:
                moves.append((piece.row,y))
            elif board[piece.row][y].team != piece.team:
                moves.append((piece.row,y))
            if (board[piece.row][y] != 0):
                break
    return moves
def R(piece, board):
    moves = []
    for i in range(1,7):
        y = piece.col+i
        
        if y in range(8):
            if board[piece.row][y] == 0:
                moves.append((piece.row,y))
            elif board[piece.row][y].team != piece.team:
                moves.append((piece.row,y))
            if (board[piece.row][y] != 0):
                break
    return moves
def FR(piece, board):
    moves = []
    for i in range(1,7):
        x = piece.row + i
        y = piece.col + i
        if x in range(8) and y in range(8):
            if board[x][y] == 0:
                moves.append((x,y))
            elif board[x][y].team != piece.team:
                moves.append((x,y))
            if (board[x][y] != 0):
                break  
    return moves
def BR(piece, board):
    moves = []
    for i in range(1,7):
        x = piece.row - i
        y = piece.col + i
        if x in range(8) and y in range(8):
            if board[x][y] == 0:
                moves.append((x,y))
            elif board[x][y].team != piece.team:
                moves.append((x,y))
            if (board[x][y] != 0):
                break  
    return moves
def BL(piece, board):
    moves = []
    for i in range(1,7):
        x = piece.row - i
        y = piece.col - i
        if x in range(8) and y in range(8):
            if board[x][y] == 0:
                moves.append((x,y))
            elif board[x][y].team != piece.team:
                moves.append((x,y))
            if (board[x][y] != 0):
                break  
    return moves
def FL(piece, board):
    moves = []
    for i in range(1,7):
        x = piece.row + i
        y = piece.col - i
        if x in range(8) and y in range(8):
            if board[x][y] == 0:
                moves.append((x,y))
            elif board[x][y].team != piece.team:
                moves.append((x,y))
            if (board[x][y] != 0):
                break  
    return moves

def pawn(piece, board):
    moves = []
    if piece.team == 'W':
        j = -1
    else:
        j = 1

    for i in [-1,1]:
        if piece.col+i in range(8):
            if board[piece.row+j][piece.col+i] != 0:
                if board[piece.row+j][piece.col+i].team != piece.team:
                    moves.append((piece.row+j,piece.col+i))
    return moves

