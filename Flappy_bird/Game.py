import pygame ,sys ,random, os

pygame.init()
current_dir = os.path.dirname(__file__)

x_scr = 816
y_scr = 725
x_f = 0
x_b = 100
y_b = y_scr/2

gravity = 0.2
bird_y_change = 0
score = 0
high_score = 0

running = False
gameover = False

scr = pygame.display.set_mode((x_scr,y_scr))

bg = pygame.image.load(os.path.join(current_dir, "Assets", "Background-night.png")).convert()
bg = pygame.transform.scale(bg,(x_scr,y_scr))
floor = pygame.transform.scale(pygame.image.load( os.path.join(current_dir, "Assets", "floor.png")).convert(),(x_scr,150))

font = pygame.font.Font(os.path.join(current_dir, '04B_19.TTF'),30)

bird_m = pygame.transform.scale(pygame.image.load( os.path.join(current_dir, "Assets", 'yellowbird-midflap.png')).convert_alpha(),(51,36))
bird_u = pygame.transform.scale(pygame.image.load( os.path.join(current_dir, "Assets", 'yellowbird-upflap.png')).convert_alpha(),(51,36))
bird_d = pygame.transform.scale(pygame.image.load( os.path.join(current_dir, "Assets", 'yellowbird-downflap.png')).convert_alpha(),(51,36))
birds = [bird_d,bird_m,bird_u]
bird_index = 1
bird = birds[1]
bird_r = bird.get_rect(center = (x_b,y_b))

pipe = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, "Assets",'pipe-green.png')).convert(),(62,600))


#timer
spawn_pipe = pygame.USEREVENT
change_bird = pygame.USEREVENT +1
pipe_list = []
pygame.time.set_timer(spawn_pipe,1200)
pygame.time.set_timer(change_bird,200)


def gamerule():
    global x_f,bird_y_change,gravity,y_b,x_f,x_scr
    bird = birds[bird_index%3]

    if running:
        bird_y_change += gravity
        bird_r.centery += bird_y_change

        x_f -= 1
        if x_f <= -x_scr:
            x_f =0


    #draw
    #else
    scr.blit(bg,(0,0))
    scr.blit(pygame.transform.rotozoom(bird,-bird_y_change*2,1),bird_r)

    #floor
    for i in pipe_list:
        i.pipe_rule()
    scr.blit(floor,(x_f,y_scr-80))
    scr.blit(floor,(x_f+x_scr,y_scr-80))

    #score
    score_draw = font.render(f'Score: {score}', True,(255,255,255))
    score_r  =score_draw.get_rect(center=(x_scr/12,y_scr/12))
    scr.blit(score_draw,score_r)

    
    

    





class pipes():
    def __init__(self,x,y):
        self.x =x
        self.y=y

        pipe_list.append(self)
    def pipe_rule(self):
        global bird_y_change,running,gameover
        self.pipe_r = pipe.get_rect(midtop = (self.x,self.y))
        self.pipe_r1 = pipe.get_rect(midtop = (self.x,self.y-750))
        if running:
            self.x -= 5
        scr.blit(pipe,self.pipe_r)
        scr.blit(pygame.transform.flip(pipe,False,True),self.pipe_r1)
        if self.x < 0:
            pipe_list.remove(self)

        #collision
        if bird_r.colliderect(self.pipe_r) or bird_r.colliderect(self.pipe_r1) or bird_r.bottom >=(y_scr-80):
            running = False
            gameover = True
            
        if bird_r.top <= 0:
            bird_y_change += 0.5
       




    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameover:
                running = True

                bird_y_change = 0
                bird_y_change -= 5
            if event.key == pygame.K_r and not running and gameover:
                gameover = False
                running = True
                pipe_list.clear()
                bird_r.center=(x_b,y_b)
                bird_y_change = 0
                bird_index = 1
                score = 0


        if event.type == spawn_pipe and running:
            score +=1
            pipe_new = pipes(1000,random.randint(200,550))
        if event.type == change_bird and running:
            bird_index += 1

    
    gamerule()

    



    pygame.display.flip()
    pygame.time.Clock().tick(120)