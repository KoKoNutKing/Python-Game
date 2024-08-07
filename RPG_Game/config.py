import pygame
import math


SCREEN_CO = (1370,725)
TITLESIZE = 32


FPS = 60

GROUND_LAYER = 1
BLOCK_LAYER = GROUND_LAYER+1
ENEMY_LAYER = BLOCK_LAYER+1
ATTACK_LAYER = ENEMY_LAYER+1
PLAYER_LAYER = ATTACK_LAYER+1
WEAPONS_LAYER = PLAYER_LAYER+1

COOLDOWN = 0.5




PLAYER_SPEED = 5
ENEMY_SPEED = 3
ARROW_SPEED = 24

tilemap = [
 '.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................BBBBBBBBBBBBBBBBBBBBBBBBBBB.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B............B............B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................BB.....B.....P.....B....BBB.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B............E............B.....................................',
'.....................................B.........................B.....................................',
'.....................................B...................E.....B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................B.........................B.....................................',
'.....................................BBBBBBBBBBBBBBBBBBBBBBBBBBB......................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',
'.....................................................................................................',




]
map_xsize = len(tilemap[0])
map_ysize = len(tilemap)

def upload_image(pic,size):
    pic = pygame.image.load(pic).convert()
    old_size = pic.get_size()
    return pygame.transform.scale(pic,(old_size[0]*(size/32),old_size[1]*(size/32)))

def center(screen_size, object_size):
    return round(screen_size/TITLESIZE/2-(object_size/2))

def facing(self,hit):
    l =(self.rect.x+ self.width) <= (hit.rect.x+hit.rect.width) and not\
                    (((self.rect.y+self.height-PLAYER_SPEED) <= hit.rect.y) or\
                    ((self.rect.y+PLAYER_SPEED) >= (hit.rect.y+hit.height)))
    r =(self.rect.x) >= (hit.rect.x) and not\
                    (((self.rect.y+self.height-PLAYER_SPEED) <= hit.rect.y) or\
                    ((self.rect.y+PLAYER_SPEED) >= (hit.rect.y+hit.height)))
    u = (self.rect.y+ self.width) <= (hit.rect.y+self.width) and not\
                    (((self.rect.x + self.width-PLAYER_SPEED) <= hit.rect.x) or\
                    ((self.rect.x+PLAYER_SPEED) >= (hit.rect.x+hit.width)))
    d = (self.rect.y) >= (hit.rect.y) and not\
                    (((self.rect.x + self.width-PLAYER_SPEED) <= hit.rect.x) or\
                    ((self.rect.x+PLAYER_SPEED) >= (hit.rect.x+hit.width)))
    return l,r,u,d


def weapons_pos(pl,mouse_pos,r,de):
    x1 , y1 = pl.x, pl.y
    x2 , y2 = mouse_pos
    # abs(x)**2+abs(y)**2=TITLESIZE

    if x1 == x2:
        x2 += 1
   
    # Các hệ số của phương trình đường thẳng
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # Giải phương trình bậc 2 để tìm nghiệm x
    A = m ** 2 + 1
    B = 2 * (m * b - m * y1 - x1)
    C = x1 ** 2 + y1 ** 2 + b ** 2 - 2 * b * y1 - r ** 2

    delta = B ** 2 - 4 * A * C

    x_1 = (-B + math.sqrt((delta))) / (2 * A)
    x_2 = (-B - math.sqrt((delta))) / (2 * A)
    y_1 = m*x_1 + b
    y_2 = m*x_2 + b

    
    
    if x2 >= x1:
        return x_1,y_1,math.degrees(math.atan(- m))+180+de
    else:
        return x_2,y_2,math.degrees(math.atan(-m))+de
    
def speed_object(pl,mouse_pos,speed):
    x1 , y1 = pl.rect.x, pl.rect.y
    x2 , y2 = mouse_pos
    x= x1-x2
    y= y1-y2
    if (math.sqrt(x**2+y**2))==0:
        c=0
    else:
        c = speed/(math.sqrt(x**2+y**2))
    return -c*x,-c*y