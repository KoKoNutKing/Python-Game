import pygame
import math
import random
from config import *

class Spritesheet():
    def __init__(self,file):
        self.sheet = upload_image(file,TITLESIZE)

    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x*(TITLESIZE/32),y*(TITLESIZE/32),width,height))
        sprite.set_colorkey("BLACK")
        return sprite
        

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self,self.groups)


        self.facing = 'right'
        self.animation_loop = 1
        self.stand_loop = 0


        self.x = x * TITLESIZE
        self.y = y * TITLESIZE


        self.x_change = 0
        self.y_change = 0

        self.height = TITLESIZE
        self.width = TITLESIZE

        self.image = self.game.test.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x =self.x
        self.rect.y = self.y

        self.weapon = Weapons(self,self.game, self.x,self.y)
        self.weapon.x = self.x
        self.weapon.y = self.y



    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_block()


        
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        for sprite in self.game.all_sprites:
            sprite.rect.x -= self.x_change
            sprite.rect.y -= self.y_change

        self.x_change = 0
        self.y_change = 0
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED

    
        



        

        
    def animate(self):
        left_stand = [self.game.test.get_sprite(0, 0, self.width, self.height),
                    self.game.test.get_sprite(96, 0, self.width, self.height),]
        
        right_stand = [self.game.test.get_sprite(0, 32, self.width, self.height),
                    self.game.test.get_sprite(96, 32, self.width, self.height),]
        
        left_animations = [self.game.test.get_sprite(0, 0, self.width, self.height),
                            self.game.test.get_sprite(32, 0, self.width, self.height),
                            self.game.test.get_sprite(64, 0, self.width, self.height),]

        right_animations = [self.game.test.get_sprite(0, 32, self.width, self.height),
                            self.game.test.get_sprite(32, 32, self.width, self.height),
                            self.game.test.get_sprite(64, 32, self.width, self.height)]

        if self.x_change == 0 and self.y_change==0:
            self.image = eval(f'{self.facing}_stand[math.floor(self.stand_loop)]')
            self.stand_loop += 0.05 
            if self.stand_loop >= 2:
                self.stand_loop = 0
        else:
            self.image = eval(f'{self.facing}_animations[math.floor(self.animation_loop)]')
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemy, False)
        if hits:
            
            for hit in hits:
                
                self.x_change = hit.x_knockback*hit.knockback
                self.y_change = hit.y_knockback*hit.knockback
           
   
               


    def collide_block(self):
  
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

        if hits:
            for hit in hits:
                l,r,u,d = facing(self,hit)
                if l:
                    if self.x_change >0:
                        self.x_change = 0
                if r:
                    if self.x_change <0:
                        self.x_change =0
                if u:
                    if self.y_change >0:
                        self.y_change = 0
                if d:
                    if self.y_change <0:
                        self.y_change = 0
   
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game,x,y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites,self.game.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TITLESIZE
        self.y = y*TITLESIZE

        self.width = TITLESIZE
        self.height = TITLESIZE

        self.x_change = 0
        self.y_change = 0


        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movement_loop = 0

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey("BLACK")

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.knockback = 3
        self.stun = 0

    def movement(self):
        p_x = self.game.player.rect.x
        p_y = self.game.player.rect.y
        chasing = False

        if (abs(self.rect.x-p_x)<= 200) and (abs(self.rect.y-p_y)<=200):
            chasing = True
        else:
            chasing = False

        if chasing:
            self.x_change,self.y_change = speed_object(self,(p_x,p_y),ENEMY_SPEED)
            self.x_knockback = self.x_change
            self.y_knockback = self.y_change


        # self.max_travel = random.randint(3,4)*TITLESIZE
        # if self.facing == 'left':
        #     self.x_change -= ENEMY_SPEED
        #     self.movement_loop -= ENEMY_SPEED
        #     if self.movement_loop <= - self.max_travel:
        #         self.facing = 'right'
        # if self.facing == 'right':
        #     self.x_change += ENEMY_SPEED
        #     self.movement_loop += ENEMY_SPEED
        #     if self.movement_loop >= self.max_travel:
        #         self.facing = 'left'
        
            

    def collide_block(self):
        
        if abs(self.x_change) > 0 :
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            
            if hits:
                if self.x_change >0:
                    self.rect.x -= ENEMY_SPEED
                if self.x_change <0:
                    self.rect.x += ENEMY_SPEED
    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.players, False)
        if hits:
            self.stun = 15


    def update(self):
        self.animate()
        self.movement()
        if self.stun == 0:
            self.rect.x += self.x_change
            self.rect.y += self.y_change
        # elif self.stun <0:
        #     self.stun =0
        else:
            self.stun -=1

            
        self.collide_block()
        self.collide_player()
        
        self.x_change = 0
        self.y_change = 0

    def animate(self):
        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        if self.x_change == 0 and self.y_change==0:
            self.image = eval(f'{self.facing}_animations[0]')
        else:
            self.image = eval(f'{self.facing}_animations[math.floor(self.animation_loop)]')
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1

class Hitboxes(pygame.sprite.Sprite):
    def __init__(self, game, x, y, size):
        self.game = game
        self._layer = ATTACK_LAYER
        self.groups = self.game.all_sprites, self.game.hitboxes
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width, self.height = size
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        

        

        self.animation_loop = 0
        self.image_load = self.game.weapons_spritesheet.get_sprite(0,64,self.width,self.height)
        self.image = self.image_load
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_e = pygame.sprite.spritecollide(self, self.game.enemy, True)
        # hits_b = pygame.sprite.spritecollide(self, self.game.blocks, True)

    def animate(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.animation_loop += 1
        if self.animation_loop >= 240:
            self.kill()
        


        



        


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TITLESIZE
        self.y = y * TITLESIZE

        self.height = TITLESIZE
        self.width = TITLESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448, self.width, self.height)
        self.rect = self.image.get_rect()

        self.rect.x =self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*TITLESIZE
        self.y = y*TITLESIZE

        self.width = TITLESIZE
        self.height = TITLESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0,352, self.width, self.height)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

class Button():
    def __init__(self, x,y,width,height,fg,bg,content,fontsize):
        self.font = pygame.font.Font('04B_19.TTF',fontsize)
        self.content = content

        self.x = x*TITLESIZE
        self.y = y*TITLESIZE
        self.width = width*TITLESIZE
        self.height = height*TITLESIZE

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
    
class Weapons(pygame.sprite.Sprite):
    def __init__(self,player,game,x,y):
        self.game = game
        self._layer = WEAPONS_LAYER

        self.groups = self.game.all_sprites, self.game.weapons
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x
        self.y = y
        self.player = player
        self.angle = 0
        self.width = TITLESIZE
        self.height = TITLESIZE

        self.animation_loop = 0
        self.cooldown = 0

        self.basic_attack = False


        self.image_load = self.game.weapons_spritesheet.get_sprite(32,32,self.width,self.height)
        self.image = self.image_load

        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.do_basic_attack()

    
    def do_basic_attack(self):
        bow_animation=     [self.game.weapons_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.weapons_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.weapons_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.weapons_spritesheet.get_sprite(0, 32, self.width, self.height),]
        self.image_load = bow_animation[math.floor(self.animation_loop)]

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        x_new,y_new,angle=weapons_pos(self.player,mouse_pos,TITLESIZE,90)

        
        self.image = pygame.transform.rotate(self.image_load,angle+90)
        self.rect.x = x_new
        self.rect.y = y_new


        if mouse_pressed[0] and self.cooldown <= 0:
            self.basic_attack = True
        if self.cooldown >0:
            self.cooldown -=1

        if self.basic_attack == True:
            self.animation_loop += 0.25
            if self.animation_loop >= 4:
                self.animation_loop = 0
                self.cooldown = COOLDOWN*FPS
                self.basic_attack = False
        if self.animation_loop == 3:
            x_arrow,y_arrow,angle_arrow=weapons_pos(self.player,mouse_pos,TITLESIZE*1.5,0)
            arrow = Hitboxes(self.game, x_arrow, y_arrow,(32,32))
            arrow.image = pygame.transform.rotate(arrow.image_load,angle_arrow+90)
            arrow.x_change,arrow.y_change = speed_object(self.player,mouse_pos,ARROW_SPEED)




            
        
        
        
            
        
