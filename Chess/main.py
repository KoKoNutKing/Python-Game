import pygame
import sys
import random
from config import *
from sprites import *

FPS = 60
screen = pygame.display.set_mode(SCREEN_CO)
pygame.display.set_caption('Chess')
pygame.init()
def get_mousrpos(pos):
    x,y = pos
    row = y // TITLESIZE
    col = x // TITLESIZE
    return row,col



def main():
    run = True
    clock = pygame.time.Clock()
    g = Game(screen)
    
    
    while run:
        clock.tick(FPS)
        play_again = Button(3,4,100,100,'WHITE','BLUE','PLAY',32)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row,col = get_mousrpos(pygame.mouse.get_pos())
                g.select(row,col)
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
        
        
                
        
            
        
        g.update()
        g.play_again()
        pygame.display.update()
    pygame.quit()
    
main()
