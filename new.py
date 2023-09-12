import pygame
import random
import sys

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Player dimensions
PLAYER_SIZE = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up display
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Load fire emoji and scared emoji images
fire_img = pygame.image.load('fire_emoji.png')
fire_img = pygame.transform.scale(fire_img, (PLAYER_SIZE, PLAYER_SIZE))
scared_img = pygame.image.load('scared_emoji.png')
scared_img = pygame.transform.scale(scared_img, (PLAYER_SIZE, PLAYER_SIZE))

# Font settings
pygame.font.init()
font = pygame.font.SysFont(None, 50)

# Player settings
player_pos = [WIDTH / 2, HEIGHT - 1.5 * PLAYER_SIZE]

# Fire settings
fire1_pos = [random.randrange(WIDTH - PLAYER_SIZE), 0]
fire2_pos = [random.randrange(WIDTH - PLAYER_SIZE), 0]
fire_speed = 2  # Reduced from 4 to 2
max_fire_speed = 4  # Reduced from 5 to 4

score = 0

# Button dimensions
button_width = 120
button_height = 60
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 2 - button_height // 2

# Restart Button dimensions
restart_button_width = 200
restart_button_height = 60
restart_button_x = WIDTH // 2 - restart_button_width // 2
restart_button_y = HEIGHT // 2 - restart_button_height // 2 + 100  # 100 pixels below the center

game_started = False
game_over = False

def detect_collision(player_pos, fire_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    f_x = fire_pos[0]
    f_y = fire_pos[1]

    if (f_x >= p_x and f_x < (p_x + PLAYER_SIZE)) or (p_x >= f_x and p_x < (f_x + PLAYER_SIZE)):
        if (f_y >= p_y and f_y < (p_y + PLAYER_SIZE)) or (p_y >= f_y and p_y < (f_y + PLAYER_SIZE)):
            return True
    return False

def draw_button():
    pygame.draw.rect(WINDOW, RED, (button_x, button_y, button_width, button_height))
    text = font.render('Play', True, WHITE)
    WINDOW.blit(text, (button_x + 30, button_y + 10))

def draw_restart_button():
    pygame.draw.rect(WINDOW, RED, (restart_button_x, restart_button_y, restart_button_width, restart_button_height))
    text = font.render('Restart', True, WHITE)
    WINDOW.blit(text, (restart_button_x + 50, restart_button_y + 10))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WINDOW.fill(BLACK)

    if game_started:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x <= WIDTH - PLAYER_SIZE:
            player_pos[0] = mouse_x

        fire1_pos[1] += fire_speed
        fire2_pos[1] += fire_speed

        if fire1_pos[1] >= HEIGHT:
            fire1_pos = [random.randrange(WIDTH - PLAYER_SIZE), 0]
            score += 1
            if fire_speed < max_fire_speed:
                fire_speed += 0.05  # Reduced from 0.5 to 0.25

        if fire2_pos[1] >= HEIGHT:
            fire2_pos = [random.randrange(WIDTH - PLAYER_SIZE), 0]
            score += 1
            if fire_speed < max_fire_speed:
                fire_speed += 0.05  # Reduced from 0.7 to 0.35

        score_text = "Score: " + str(score)
        label = font.render(score_text, 1, WHITE)
        WINDOW.blit(label, (WIDTH - 200, HEIGHT - 40))

        if detect_collision(player_pos, fire1_pos) or detect_collision(player_pos, fire2_pos):
            score = 0
            game_over_text = "Game Over!"
            game_over_label = font.render(game_over_text, 1, WHITE)
            WINDOW.blit(game_over_label, (WIDTH / 2 - 100, HEIGHT / 2))
            pygame.display.update()
            pygame.time.delay(2000)
            fire1_pos = [random.randrange(WIDTH - PLAYER_SIZE), 0]
            fire2_pos = [random.randrange(WIDTH - PLAYER_SIZE), 0]
            fire_speed = 2  # Keep the speed consistent with initial speed
            game_started = False
            game_over = True

        WINDOW.blit(fire_img, (fire1_pos[0], fire1_pos[1]))
        WINDOW.blit(fire_img, (fire2_pos[0], fire2_pos[1]))
        WINDOW.blit(scared_img, (player_pos[0], player_pos[1]))

    elif game_over:  # if game is over, show restart button
        draw_restart_button()

        # Check if the restart button is pressed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if restart_button_x <= mouse_x <= restart_button_x + restart_button_width and restart_button_y <= mouse_y <= restart_button_y + restart_button_height:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:  # Left mouse button
                game_started = True
                game_over = False
                fire_speed = 2  # Keep the speed consistent with initial speed
                score = 0

    else:
        draw_button()

        # Check if the button is pressed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:  # Left mouse button
                game_started = True

    pygame.display.update()
