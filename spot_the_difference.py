#SPOT_THE_DIFFERENCE
import pygame

#initialize pygame
pygame.init()

#game folder
GAME_FOLDER = "D:/batches/Python Ground Up/Video Games/spot_the_difference/"

#game window (display_surface)
HUD_HEIGHT = 60
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 740 + HUD_HEIGHT

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#colors
RED = pygame.Color(255,0,0)
BLUE = pygame.Color(0,0,255)
ORANGE = pygame.Color(255,127,0)
BLACK = pygame.Color(0,0,0)

RADIUS = 20


differences = {
    ((680,245,750,285),): 0,
    ((850,210,910,250),): 0,
    ((700,600,840,700),): 0,
    ((835,375,875,415),): 0,
    ((888,390,910,430), (935,410,965,450)): 0,
    ((520,670,580,720),): 0,
    ((820,550,870,590),): 0,
    ((550,425,615,490),): 0,
    ((855,685,895,720),): 0,
    ((760,80,780,115), (790,100,815,130), (820,110,845,135), (840,135,860,185), (815,180,830,200)): 0
}
user_selection = {}

#load the background image/ game canvas
game_canvas = pygame.image.load(GAME_FOLDER + "spot_the_difference.jpg")

#loading the sounds
pickup = pygame.mixer.Sound(GAME_FOLDER + "pickup.wav")
pickup.set_volume(0.5)
loss = pygame.mixer.Sound(GAME_FOLDER + "loss.wav")
loss.set_volume(0.5)
tick = pygame.mixer.Sound(GAME_FOLDER + "tick.wav")
loss.set_volume(1)
beep = pygame.mixer.Sound(GAME_FOLDER + "beep.wav")
beep.set_volume(1)

#timer
timer = 60
frame_time = 0

#fonts and text

font_big = pygame.font.Font(GAME_FOLDER + "SunnyspellsRegular.otf",60)
font_small = pygame.font.Font(GAME_FOLDER + "SunnyspellsRegular.otf",40)

title = font_big.render("Spot The Difference", True, ORANGE)
title_rect = title.get_rect()
title_rect.center = (WINDOW_WIDTH//2,HUD_HEIGHT//2)

game_timer = font_small.render("Play time: " + str(timer), True, ORANGE)
game_timer_rect = game_timer.get_rect()
game_timer_rect.left = 50
game_timer_rect.centery = HUD_HEIGHT//2

selections = font_small.render("Selections: " + str(len(user_selection)) + "/" + str(len(differences)), True, ORANGE)
selections_rect = selections.get_rect()
selections_rect.right = WINDOW_WIDTH-50
selections_rect.centery = HUD_HEIGHT//2

game_over = font_big.render("Game Over, You Lose!!!", True, RED)
game_over_rect = game_over.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2- 50)

game_replay_quit = font_small.render("Press R to Replay or Q to Quit", True, BLUE)
game_replay_quit_rect = game_replay_quit.get_rect()
game_replay_quit_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+50)

#main game loop
game_status = 1
running = True
FPS = 30
clock = pygame.time.Clock()

while running: #main game loop (defines the life of the game)

    #Fetch the captured events
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN and game_status == 0:
            if ev.key == pygame.K_q:
                running = False
            elif ev.key == pygame.K_r:
                timer = 60
                user_selection.clear()
                game_timer = font_small.render("Play time: " + str(timer), True, ORANGE)
                game_over = font_big.render("Game Over, You Lose!!!", True, RED)
                selections = font_small.render("Selections: " + str(len(user_selection)) + "/" + str(len(differences)), True,ORANGE)
                for a_diff in differences:
                    differences[a_diff]= 0
                game_status = 1

        elif ev.type == pygame.MOUSEBUTTONDOWN and game_status == 1:
            if ev.button == pygame.BUTTON_LEFT:
                #fetch the coords of click
                x,y = ev.pos
                #limit the area of click to right half and below the HUD height
                if x >0 and x <= WINDOW_WIDTH//2 or y > 0 and y <HUD_HEIGHT:
                    continue

                #check for x,y in differences and update the differences accordingly
                color = RED
                for a_diff in differences:
                    for a_region in a_diff:
                        if x >= a_region[0] and x <= a_region[2]:
                            if y-HUD_HEIGHT >= a_region[1] and y-HUD_HEIGHT <= a_region[3]:
                                differences[a_diff] += 1
                                color = BLUE if differences[a_diff] == 1 else None
                                break
                if color is not None:
                    if color == RED:
                        loss.play()
                    elif color == BLUE:
                        pickup.play()
                    coords = (x-RADIUS, y-RADIUS, 2*RADIUS, 2*RADIUS)
                    #dict[new_key] = value
                    user_selection[coords] = color
                    selections = font_small.render("Selections: " + str(len(user_selection)) + "/" + str(len(differences)), True, ORANGE)

                if len(user_selection) == len(differences):
                    flag = 1
                    for a_diff in differences:
                        if differences[a_diff] == 0:
                            flag = 0
                            break
                    if flag == 1:
                        game_over = font_big.render("Game Over, You Win!!!", True, RED)

                    game_status = 0


    # blit the HUD (Heads Up Display)
    window.fill(BLACK, (0,0, WINDOW_WIDTH, HUD_HEIGHT))
    window.blit(title, title_rect)
    window.blit(selections, selections_rect)
    window.blit(game_timer, game_timer_rect)

    # blit the game canvas
    window.blit(game_canvas, (0, HUD_HEIGHT))

    # draw the user selections
    for coords in user_selection:
        #ellipse (canvas, color, coords, thickness)
        pygame.draw.ellipse(window, user_selection[coords], coords, 5)

    if game_status == 1:
        frame_time += 1
        if frame_time == FPS:
            frame_time = 0
            timer -= 1
            game_timer = font_small.render("Play time: " + str(timer), True, ORANGE)

            if timer < 10:
                beep.play()
            else:
                tick.play()
            if timer == 0:
                game_status = 0#game ends
    elif game_status == 0:
        window.blit(game_over, game_over_rect)
        window.blit(game_replay_quit, game_replay_quit_rect)

    #refresh the display
    pygame.display.update()

    #regulates the loop cycles to set FPS, to ensure minimum CPU utilization
    #provides the same playing experience over different CPU's
    clock.tick(FPS)

#quit pygame
pygame.quit()
