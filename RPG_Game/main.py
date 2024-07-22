import pygame
import sys
from sprite import *
from config import *



class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_CO,pygame.RESIZABLE )        
        self.width, self.height = self.screen.get_size()
        self.center_x = center(self.width,map_xsize)
        self.center_y = center(self.height,map_ysize)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('04B_19.TTF',32)
        self.running = True

        self.character_spritesheet = Spritesheet('D:/Code/Python/RPG_GAME/img/character.png')
        self.enemy_spritesheet = Spritesheet('D:\Code\Python\RPG_GAME\img\enemy.png')
        self.attack_spritesheet = Spritesheet('D:\Code\Python\RPG_GAME\img/attack.png')
        self.terrain_spritesheet = Spritesheet('D:/Code/Python/RPG_GAME/img/terrain.png')
        self.test = Spritesheet('D:/trash/my_sprite.png')
        self.weapons_spritesheet = Spritesheet('D:/trash/weapons.png')

        self.intro_bg = pygame.transform.scale(pygame.image.load("img\introbackground.png")\
            .convert(),(self.width,self.height))
        self.outro_bg = pygame.transform.scale(pygame.image.load("img\gameover.png")\
            .convert(),(self.width,self.height))


    def createTilemap(self):
        
        for i, row in enumerate(tilemap):
            i += self.center_y

            for j, column in enumerate(row):
                j+=self.center_x
                Ground(self,j,i)

                if column == "B":
                    Block(self,j,i)
                if column == "P":
                    self.player = Player(self,j,i)

                if column == "E":
                    Enemy(self,j,i)



    def new(self):
        #New game start

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.hitboxes = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()

        self.createTilemap()
        
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False 
            # if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
            #             if self.player.facing == 'up':
            #                 Hitboxes(self, self.player.rect.x, self.player.rect.y-TITLESIZE,(8,29))
            #             if self.player.facing == 'down':
            #                 Hitboxes(self, self.player.rect.x, self.player.rect.y+TITLESIZE,(8,29))
            #             if self.player.facing == 'left':
            #                 Hitboxes(self, self.player.rect.x - TITLESIZE, self.player.rect.y,(8,29))
            #             if self.player.facing == 'right':
            #                 Hitboxes(self, self.player.rect.x + TITLESIZE, self.player.rect.y,(8,29))

    def update(self):
        self.all_sprites.update()
    def draw(self):
        self.screen.fill("BLACK")
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        pygame.display.update()
    def main(self):
        # game loop
        while self.playing:
            self.event()
            self.update()
            self.draw()
    def game_over(self):
        text = self.font.render('Game Over',True, "WHITE")
        text_tect = text.get_rect(center=(self.width/2,self.height/2))
        restart_button = Button(3,center(self.height,4),6,4,'WHITE','BLACK','Restart',32)
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                

            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_press(mouse_pos,mouse_pressed) or keys[pygame.K_SPACE]:
                self.new()
                self.main()     

            self.screen.blit(self.outro_bg,(0,0))
            self.screen.blit(text, text_tect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
        
    def intro_screen(self):
        intro = True


        play_button = Button(center(self.width,6),center(self.height,4),6,4,'WHITE','BLACK','Play',32)

        while intro:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_press(mouse_pos,mouse_pressed) or keys[pygame.K_SPACE]:
                intro = False

            self.screen.blit(self.intro_bg,(0,0))
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()