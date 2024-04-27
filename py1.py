import pygame
import time
import random
from sys import exit
random.seed(42)

# set up pygame window
WIDTH = 500
HEIGHT = 500
GRID_WIDTH=50
FPS = 60

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
quit_flag=False
retry_g=False
wc=False

# initalise Pygame
pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Game")
clock = pygame.time.Clock()
dt = 0

COUNTDOWN_SECONDS = 100
countdown_timer = COUNTDOWN_SECONDS * 1000  # Convert seconds to milliseconds
# start_time = pygame.time.get_ticks()
start_time=0

whites= pygame.Surface((WIDTH+1000,HEIGHT+1000))
whites.fill(WHITE)
maze = pygame.Surface((2000, 2000))
levels = ['Easy', 'Medium', 'Hard']  # Define available levels
selected_level = None
bigplayer = pygame.image.load('python.jpg').convert()
img_width=50
img_height=50
player = pygame.transform.scale(bigplayer,(img_width,img_height))
player_pos = pygame.Vector2(245, 245)
random_xs = [random.randint(0, 20)*100+25 for _ in range(3)]
random_ys = [random.randint(0, 20)*100+25 for _ in range(3)]
red_die1=pygame.image.load('red_die.jpg').convert()
red_die2=pygame.transform.scale(red_die1,(img_width,img_height))
pygame.display.flip()
# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 100                   # width of cell
grid = []
visited = []
stack = []
solution = {}
# lines_exit=np.array()

font = pygame.font.Font(None, 36)

def draw_opening_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Welcome to My Game", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))

    y_button=250

    # Display level options
    for level in levels:
            # Draw buttons
        button_width, button_height = 200, 50
        start_button_rect = pygame.Rect(WIDTH//2 - button_width//2, y_button, button_width, button_height)
        pygame.draw.rect(screen, GREEN, start_button_rect)
        start_text = font.render(level, True, WHITE)
        screen.blit(start_text, (start_button_rect.centerx - start_text.get_width()//2, start_button_rect.centery - start_text.get_height()//2))
        y_button+=50
       

    pygame.display.flip()

# Function to check for button clicks
def check_button_click(pos):
    y_button_rect=250
    for level in levels:
        start_button_rect = pygame.Rect(WIDTH//2 - 100, y_button_rect, 200, 50)
        if start_button_rect.collidepoint(pos):
            return True
        y_button_rect+=50
    return False


# Function to draw the game over screen
def draw_game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 100))

    # Display score or any other relevant information
    score_text = font.render("Your Score: 100", True, BLACK)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))

    # Draw a button to play again
    button_width, button_height = 200, 50
    play_again_button_rect = pygame.Rect(WIDTH//2 - button_width//2, 300, button_width, button_height)
    pygame.draw.rect(screen, RED, play_again_button_rect)
    play_again_text = font.render("Play Again", True, WHITE)
    screen.blit(play_again_text, (play_again_button_rect.centerx - play_again_text.get_width()//2, play_again_button_rect.centery - play_again_text.get_height()//2))

    pygame.display.flip()


def draw_oops_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Oops!", True, BLACK)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 100))

    # Display score or any other relevant information
    score_text = font.render("You Lost, Better Luck Next Time", True, BLACK)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))

    # Draw a button to play again
    button_width, button_height = 200, 50
    play_again_button_rect = pygame.Rect(WIDTH//2 - button_width//2, 300, button_width, button_height)
    pygame.draw.rect(screen, RED, play_again_button_rect)
    play_again_text = font.render("Retry", True, WHITE)
    screen.blit(play_again_text, (play_again_button_rect.centerx - play_again_text.get_width()//2, play_again_button_rect.centery - play_again_text.get_height()//2))

    pygame.display.flip()

def draw_wrong_corner_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Oh No!", True, BLACK)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 100))

    # Display score or any other relevant information
    score_text = font.render("You have reached the Devil's home, RIP", True, BLACK)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))

    # Draw a button to play again
    button_width, button_height = 200, 50
    play_again_button_rect = pygame.Rect(WIDTH//2 - button_width//2, 300, button_width, button_height)
    pygame.draw.rect(screen, RED, play_again_button_rect)
    play_again_text = font.render("Retry", True, WHITE)
    screen.blit(play_again_text, (play_again_button_rect.centerx - play_again_text.get_width()//2, play_again_button_rect.centery - play_again_text.get_height()//2))

    pygame.display.flip()

# Function to check for button clicks on the game over screen
def check_play_again_click(pos):
    play_again_button_rect = pygame.Rect(WIDTH//2 - 100, 300, 200, 50)
    if play_again_button_rect.collidepoint(pos):
        return True
    return False

# build the grid
def build_grid(x, y, w):
    y-=w
    for i in range(1,21):
        x = 0                                                            # set x coordinate to start position
        y = y + w                                                        # start a new row
        for j in range(1, 21):
            pygame.draw.line(maze, WHITE, [x, y], [x + w, y],1)           # top of cell
            pygame.draw.line(maze, WHITE, [x + w, y], [x + w, y + w],1)   # right of cell
            pygame.draw.line(maze, WHITE, [x + w, y + w], [x, y + w],1)   # bottom of cell
            pygame.draw.line(maze, WHITE, [x, y + w], [x, y],1)           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + w                                                    # move cell to new position

width=1
def push_up(x, y):
    pygame.draw.rect(maze, BLACK, (x + width, y - w + width, w-width, 2*w-width), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(maze, BLACK, (x + width, y + width, w-width, 2*w-width), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(maze, BLACK, (x - w +width, y +width, 2*w-width, w-width), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(maze, BLACK, (x +width, y +width, 2*w-width, w-width), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(maze, GREEN, (x +width, y +width, w-width, w-width), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(maze, BLACK, (x +width, y +width, w-width, w-width), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(x,y):
    pygame.draw.rect(maze, YELLOW, (x+8, y+8, 5, 5), 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell


def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack=[]
    visited=[]
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                push_right(x, y)                                   # call push_right function
                solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            #time.sleep(.05)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path


def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (0,0):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back

def get_color(x, y):
    # Get the color of the pixel at (x, y)
    color=screen.get_at((x,y))
    return color

def red_die():
    red_die1=pygame.image.load('red_die.jpg').convert()
    red_die2=pygame.transform.scale(red_die1,(img_width,img_height))
    screen.blit(red_die1,(maze_x+random_x, maze_y+random_y))


def mazef(surface):
    maze.fill(BLACK)
    x, y = 0, 0                     # starting position of grid
    build_grid(0, 0, w)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
    carve_out_maze(x,y)               # call build the maze  function
    # plot_route_back(19*w,19*w)         # call the plot solution function

    screen.blit(maze,(maze_x,maze_y))
    return maze

maze_x= 20 - 20*50
maze_y=20 - 20*50

def game():    
    global maze_x, maze_y, wc,countdown_timer
    maze_x= 20 - 20*50
    maze_y=20 - 20*50

    mazef(maze)

    page2 = True
    screen.blit(player, (player_pos.x,player_pos.y))

    while page2:
        global retry_g
        global wc
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               exit()

        # elapsed_time=0
    
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, countdown_timer - elapsed_time)
        seconds = remaining_time // 1000

        if seconds > 10:
            text = font.render(f"Time: {seconds}", True, GREEN)
        else:
            text = font.render(f"Time: {seconds}", True, RED)
        
        text_rect = text.get_rect(center=(WIDTH // 10, HEIGHT // 10))
        screen.blit(maze,(maze_x,maze_y))
        screen.blit(player, (player_pos.x,player_pos.y))
        for random_x, random_y in zip(random_xs, random_ys):
            screen.blit(red_die2,(maze_x+random_x, maze_y+random_y))
        screen.blit(text, text_rect)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        movement=50
        sleep_time=0.1
        if keys[pygame.K_w]:
            screen.blit(whites,(0,0))
            maze_y+=movement
            screen.blit(maze,(maze_x,maze_y))
            time.sleep(sleep_time)
            screen.blit(whites,(0,0))
            screen.blit(maze,(maze_x,maze_y))
            # print(get_color(int(player_pos.x),int(player_pos.y+img_height/2)))
            if get_color(int(player_pos.x),int(player_pos.y+img_height/2))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2), int(player_pos.y))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2),int(player_pos.y+img_height/2))== (255,255,255,255):
                maze_y-=movement
                screen.blit(whites,(0,0))
                screen.blit(maze,(maze_x,maze_y) )
            screen.blit(player, (player_pos.x,player_pos.y))
            for random_x, random_y in zip(random_xs, random_ys):
                screen.blit(red_die2,(maze_x+random_x, maze_y+random_y))
                print(maze_x, maze_y, random_x, random_y)
         
        if keys[pygame.K_s]:
            screen.blit(whites,(0,0))
            maze_y-=movement
            screen.blit(maze,(maze_x,maze_y))
            time.sleep(sleep_time)
            screen.blit(whites,(0,0))
            screen.blit(maze,(maze_x,maze_y))
            if get_color(int(player_pos.x),int(player_pos.y+img_height/2))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2), int(player_pos.y))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2),int(player_pos.y+img_height/2))== (255,255,255,255):
                maze_y+=movement
                screen.blit(whites,(0,0))
                screen.blit(maze,(maze_x,maze_y) )
            screen.blit(player, (player_pos.x,player_pos.y))
            for random_x, random_y in zip(random_xs, random_ys):
                screen.blit(red_die2,(maze_x+random_x, maze_y+random_y))
           
        if keys[pygame.K_a]:
            screen.blit(whites,(0,0))
            maze_x+=movement
            screen.blit(maze,(maze_x,maze_y))
            time.sleep(sleep_time)
            screen.blit(whites,(0,0))
            screen.blit(maze,(maze_x,maze_y))
            if get_color(int(player_pos.x+img_width/2),int(player_pos.y))== (255,255,255,255) or get_color(int(player_pos.x), int(player_pos.y+img_height/2))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2),int(player_pos.y+img_height/2))== (255,255,255,255):
                maze_x-=movement
                screen.blit(whites,(0,0))
                screen.blit(maze,(maze_x,maze_y) )
            screen.blit(player, (player_pos.x,player_pos.y))
            for random_x, random_y in zip(random_xs, random_ys):
                screen.blit(red_die2,(maze_x+random_x, maze_y+random_y))

        if keys[pygame.K_d]:
            screen.blit(whites,(0,0))
            maze_x-=movement
            screen.blit(maze,(maze_x,maze_y))
            time.sleep(sleep_time)
            screen.blit(whites,(0,0))
            screen.blit(maze,(maze_x,maze_y))
            if get_color(int(player_pos.x+img_width/2),int(player_pos.y))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2), int(player_pos.y))== (255,255,255,255) or get_color(int(player_pos.x+img_width/2),int(player_pos.y+img_height/2))== (255,255,255,255):
                maze_x+=movement
                screen.blit(whites,(0,0))
                screen.blit(maze,(maze_x,maze_y) )
            screen.blit(player, (player_pos.x,player_pos.y))
            for random_x, random_y in zip(random_xs, random_ys):
                screen.blit(red_die2,(maze_x+random_x, maze_y+random_y))

        for random_x, random_y in zip(random_xs, random_ys):
            if random_x+maze_x==245 and random_y+maze_y==245:
                random_xs.remove(random_x)
                random_ys.remove(random_y)
                random_number = random.randint(1, 6)
                COUNTDOWN_SECONDS = 100-random_number*2
                countdown_timer = COUNTDOWN_SECONDS * 1000
            

        # print(maze_x,maze_y)

        if maze_x == 220 - 38*movement and maze_y == 220 - 38*movement:
            maze_x= 20 - 20*50
            maze_y=20 - 20*50
            
            break 

        
        if maze_x == 220 - 38*movement and maze_y == 220:
            wc=True
            maze_x= 20 - 20*50
            maze_y=20 - 20*50
            break
        
        if maze_x == 220 and maze_y == 220 - 38*movement:
            wc=True
            maze_x= 20 - 20*50
            maze_y=20 - 20*50
            break

        if maze_x == 220 and maze_y == 220:
            wc=True
            maze_x= 20 - 20*50
            maze_y=20 - 20*50
            break


        if remaining_time == 0:
            # Add code to handle what happens when the countdown ends
            retry_g=True
            break

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    # elapsed_time=0

def game_by_level(game_level):
    global COUNTDOWN_SECONDS, countdown_timer
    if game_level== levels[0]:
        COUNTDOWN_SECONDS = 100
        countdown_timer = COUNTDOWN_SECONDS * 1000
        game()
        
    elif game_level== levels[1]:
        COUNTDOWN_SECONDS = 150
        countdown_timer = COUNTDOWN_SECONDS * 1000
        game()
        hole1 = pygame.image.load('hole1.jpg').convert()
        hole_width=50
        hole_height=50
        hole2 = pygame.transform.scale(hole1,(hole_width,hole_height))
        retry_game()
        #time.sleep(1)
        maze.blit(hole2,(220 - 38*50, 220 - 38*50))
        game()

    elif game_level== levels[2]:
        COUNTDOWN_SECONDS = 175
        countdown_timer = COUNTDOWN_SECONDS * 1000
        game()
        retry_game()
        game()
        retry_game()
        game()
 

def start_game():
    global start_time
    sg=True
    while sg: 
        draw_opening_screen()
        for event in pygame.event.get():  
            # check for closing the window
            if event.type == pygame.QUIT:
                exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:  # Left mouse button
                    click_pos = pygame.mouse.get_pos()
                    if check_button_click(click_pos):
                        for i, level in enumerate(levels):
                            if (250+i*50)< click_pos[1] <(300+i*50):
                                selected_level = level
                                print("Starting game...")
                                print("Chosen level: ", level)
                                start_time = pygame.time.get_ticks()

                                game_by_level(selected_level)
                            
                                return
                        if selected_level is not None:
                            return selected_level

            #else: break

def replay():
     global wc, retry_g
     for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    click_pos = pygame.mouse.get_pos()
                    if check_play_again_click(click_pos):
                        
                        print("Starting game...")
                        retry_g=False
                        wc=False

                        start_game()
            #else:break

def reset_game():
    global rg, wc, retry_g
    rg=True
    while rg:
        draw_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    click_pos = pygame.mouse.get_pos()
                    if check_play_again_click(click_pos):
                        
                        print("Starting game...")

                        start_game()
            #else:break

def retry_game():
    global wc,retry_g
    while retry_g:
        draw_oops_screen()
        replay()

    while wc:
        draw_wrong_corner_screen()
        replay()


# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)

    start_game()
    retry_game()
    reset_game()

    
pygame.quit()