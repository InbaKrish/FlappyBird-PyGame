import pygame, sys, random

def set_bg():
    b = ["bluebird", "redbird", "yellowbird"]
    birdtype = str(random.choice(b))
    birdtype = 'assets/' + birdtype
    if birdtype != 'assets/redbird' or birdtype == 'assets/yellowbird':
        bg_image = pygame.image.load('assets/background-day.png').convert()
        #scales the bg_image loaded in the above line
        bg_image = pygame.transform.scale(bg_image, (432, 768))

        pipe = pygame.image.load('assets/pipe-green.png').convert()
        pipe = pygame.transform.scale(pipe, (int(pipe.get_width() * 1.5), int(pipe.get_height() * 1.5)))
    else:
        bg_image = pygame.image.load('assets/background-night.png').convert()
        #scales the bg_image loaded in the above line
        bg_image = pygame.transform.scale(bg_image, (432, 768))

        pipe = pygame.image.load('assets/pipe-red.png').convert()
        pipe = pygame.transform.scale(pipe, (int(pipe.get_width() * 1.5), int(pipe.get_height() * 1.5)))
    
    return bg_image,pipe

def set_birds():
    b = ["bluebird", "redbird", "yellowbird"]
    birdtype = str(random.choice(b))
    birdtype = 'assets/' + birdtype

    bird_midflap = pygame.transform.scale(pygame.image.load(
        birdtype+'-midflap.png').convert_alpha(), (int(34 * 1.2), int(24 * 1.2)))
    bird_upflap = pygame.transform.scale(pygame.image.load(
        birdtype + '-upflap.png').convert_alpha(), (int(34 * 1.2), int(24 * 1.2)))
    bird_downflap = pygame.transform.scale(pygame.image.load(
        birdtype + '-downflap.png').convert_alpha(), (int(34 * 1.2), int(24 * 1.2)))
    birds = [bird_upflap, bird_midflap, bird_downflap]

    return birds

def move_floor():
    screen.blit(floor, (floor_x_position, 660))
    screen.blit(floor, (floor_x_position + 432, 660))

def put_pipes(pipe_rects):
    for pipe_rect in pipe_rects:
        if pipe_rect.bottom >= 768:
            screen.blit(pipe, pipe_rect)
        else:
            flippipe = pygame.transform.flip(pipe, False, True)
            screen.blit(flippipe,pipe_rect)
        
def move_pipes(pipe_rects):
    for pipe_rect in pipe_rects:
        pipe_rect.centerx -= 5
    return pipe_rects

def create_pipe_rects():
    height = random.choice(pipe_heights)
    bottom_pipe = pipe.get_rect(midtop=(450, height))
    top_pipe = pipe.get_rect(midbottom = (450, height - 200))
    pipe_rects.extend((bottom_pipe,top_pipe))
    return pipe_rects

def collision_check(pipe_rects):
    for pipe_rect in pipe_rects:
        if bird_rect.colliderect(pipe_rect):
            death_sound.play()
            birds = set_birds()
            return False
    
    if bird_rect.bottom >= 660 or bird_rect.top <= -50:
        death_sound.play()
        birds = set_birds() 
        return False

    return True

def rotate_bird(bird):
    rbird = pygame.transform.rotozoom(bird, -(bird_movement*2), 1)
    return rbird

def animate_bird():
    new_bird = birds[bird_anim_index]
    new_bird_rect = new_bird.get_rect(center=(60, bird_rect.centery))
    return new_bird, new_bird_rect

def display_score():
    if game_status:
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 80))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 80))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score : {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 610))
        screen.blit(high_score_surface, high_score_rect)

        gameover_rect = gameover.get_rect(center=(216, 300))
        screen.blit(gameover, gameover_rect)
        
        restart_surface = game_font.render(
            f'Press Space to START', True, (220, 40, 40))
        restart_rect = restart_surface.get_rect(center=(216, 730))
        screen.blit(restart_surface, restart_rect)

        bg_image = set_bg()
        birds = set_birds()

#initialize the pygame
pygame.init()
pygame.mixer.pre_init(channels=1, buffer=512)


#sets the default canvas screen
screen = pygame.display.set_mode((432, 768))
game_font = pygame.font.Font('04B_19.ttf', 30)
name_font = pygame.font.Font('04B_19.ttf', 14)

#game variables
gravity_factor = 0.18
game_status = True  #used to check the game's status
score = 0
high_score = 0

floor = pygame.image.load('assets/base.png').convert()
floor = pygame.transform.scale(floor, (504, 168))
floor_x_position = 0

bird_anim_index = 0
bird_movement = 0
birds = set_birds()
bird = birds[bird_anim_index]
bird_rect = bird.get_rect(center=(60, 384))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

bg_image, pipe = set_bg()

pipe_rects = []
PLACEPIPETIMER = pygame.USEREVENT                         #timer variable activates on user event timer
pygame.time.set_timer(PLACEPIPETIMER, 1200)  #sets timer 
pipe_heights = [300, 380, 500]

gameover = pygame.transform.scale(pygame.image.load('assets/message.png').convert_alpha(), (int(184* 1.2), int(267* 1.2)))
fly_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

#pygame's clock 
clock = pygame.time.Clock()

while True:

    #loop gets all the event from the user (eg.mouse input,keyboard input,etc.)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:   #this event is the exit button input
            pygame.quit()               #quits pygame
            sys.exit()  #ends the screen in a proper way

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_status:
                bird_movement = 0
                bird_movement -= 8
                fly_sound.play()
            if event.key == pygame.K_SPACE and game_status == False:
                bg_image, pipe = set_bg()
                birds = set_birds() 
                game_status = True
                bird_rect.center = (60, 384)
                pipe_rects.clear()
                bird_movement = 0
                score = 0

        if event.type == PLACEPIPETIMER:
            pipe_rects = create_pipe_rects()
        
        if event.type == BIRDFLAP:
            if bird_anim_index < 2:
                bird_anim_index += 1
            else:
                bird_anim_index = 0

            bird,bird_rect = animate_bird()

    screen.blit(bg_image, (0, 0))  #sets the bg_image to the surface 

    if game_status:
        #bird
        bird_movement += gravity_factor
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)
        game_status = collision_check(pipe_rects)

        #pipes
        pipe_rects = move_pipes(pipe_rects)
        put_pipes(pipe_rects)
        
        score += 0.0075
        
        if score > high_score:
            high_score = score
        
        display_score()

    #floor
    floor_x_position -= 1
    move_floor()
    if floor_x_position <= -432:
        floor_x_position = 0

    score_surface = name_font.render("By Inbakrish", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(50, 25))
    screen.blit(score_surface, score_rect)
    
    display_score()
    pygame.display.update()  #updates the screen with the things in the loop 
    clock.tick(90)           #sets the frame rate limit to 90 , so that it doesnt exeeds 90fps
