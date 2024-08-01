import pygame
import sys
import random
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

FPS = 60  # Frames per second
WIDTH, HEIGHT = 1220, 720  # Window dimensions

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babunia")

# Load images
menu_bg = pygame.transform.scale(pygame.image.load("menu.png"), (WIDTH, HEIGHT))
trawka = pygame.transform.scale(pygame.image.load("trawka.png"), (100, 100))
dom = pygame.transform.scale(pygame.image.load('dom.png'), (200, 200))
dom_world_pos = (1000, 1000)
dom_rect = dom.get_rect(topleft=dom_world_pos)

standing_right = pygame.transform.scale(pygame.image.load("PanPole.png"), (200, 200))
step_right = pygame.transform.scale(pygame.image.load("2.png"), (200, 200))
standing_left = pygame.transform.scale(pygame.image.load("3.png"), (200, 200))
step_left = pygame.transform.scale(pygame.image.load("5.png"), (200, 200))
standing_down = pygame.transform.scale(pygame.image.load("1.png"), (200, 200))
step_down1 = pygame.transform.scale(pygame.image.load("7.png"), (200, 200))
step_down2 = pygame.transform.scale(pygame.image.load("8.png"), (200, 200))
standing_up = pygame.transform.scale(pygame.image.load("9.png"), (200, 200))
step_up1 = pygame.transform.scale(pygame.image.load("10.png"), (200, 200))
step_up2 = pygame.transform.scale(pygame.image.load("11.png"), (200, 200))

# Initial player position next to the house
player_world_pos = pygame.Vector2(dom_world_pos[0] + 250, dom_world_pos[1])

# Enemy image
enemy_image = pygame.transform.scale(pygame.image.load("babunia.png"), (200, 200))
enemy_world_pos = pygame.Vector2(300, 300)

# Random trawka positions
num_trawka = 17
trawka_positions = [(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)) for _ in range(num_trawka)]
additional_trawka = pygame.transform.scale(pygame.image.load("drzewo.png"), (100, 100))
trawka_rects = [additional_trawka.get_rect(topleft=pos) for pos in trawka_positions]

# Random kamper positions
num_kamper = 1
kamper_positions = [(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)) for _ in range(num_kamper)]
additional_kamper = pygame.transform.scale(pygame.image.load("kamper.png"), (200, 200))
kamper_rects = [additional_kamper.get_rect(topleft=pos) for pos in kamper_positions]

# Animation variables
left, right, up, down, is_step, facing_right, facing_up, facing_down = False, False, False, False, False, True, False, False
player_speed = 4
enemy_speed = 6

# Camera position
camera_pos = pygame.Vector2(player_world_pos.x - WIDTH // 2, player_world_pos.y - HEIGHT // 2)

# Clock settings
start_time = datetime.strptime("08:00 AM", "%I:%M %p")
end_time = datetime.strptime("12:00 PM", "%I:%M %p")
current_time = start_time

# Font for the clock and task list
font = pygame.font.Font(None, 36)

# Tasks
tasks = ["Idź na kebsa"]
tasks_completed = [False]


# Function to draw text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Function to draw tasks on screen
def draw_tasks(tasks, tasks_completed, font, color, surface, x, y):
    for i, task in enumerate(tasks):
        task_text = f"{'[X]' if tasks_completed[i] else '[ ]'} {task}"
        draw_text(task_text, font, color, surface, x, y + i * 30)


# Game over screen
def draw_game_over():
    WIN.fill(WHITE)
    draw_text("GAME OVER", font, BLACK, WIN, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    pygame.draw.rect(WIN, BROWN, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
    draw_text("Restart", font, WHITE, WIN, WIDTH // 2 - 50, HEIGHT // 2 + 10)
    pygame.draw.rect(WIN, BROWN, (WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50))
    draw_text("Exit", font, WHITE, WIN, WIDTH // 2 - 30, HEIGHT // 2 + 70)
    pygame.display.update()


# Main menu screen
def draw_main_menu():
    WIN.blit(menu_bg, (0, 0))
    pygame.draw.rect(WIN, BROWN, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
    draw_text("Start Game", font, WHITE, WIN, WIDTH // 2 - 70, HEIGHT // 2 + 10)
    pygame.draw.rect(WIN, BROWN, (WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50))
    draw_text("Exit", font, WHITE, WIN, WIDTH // 2 - 30, HEIGHT // 2 + 70)

    # Display the rotating message at the bottom
    draw_text(rotating_message, font, (255, 255, 0), WIN, WIDTH // 2 - 100,
              HEIGHT - 50)  # Adjusted position for the message

    pygame.display.update()


# Collision checking function
def check_collisions(rect, obstacles):
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            return True
    return False


# Main game loop
running = True
in_game = False
game_over = False
clock = pygame.time.Clock()
time_elapsed_since_last_action = 0
time_elapsed_for_clock_update = 0
enemy_active = False

# Rotating messages
rotating_messages = [
    "Also Try RocketMan Adventures!",
    "Now with more kebabs!",
    "Watch out for Babunia!",
    "Stay inside the trawka!",
    "Bober is my life"
    "Bober is the best with skin"
    "don't be colorful"
    "how are your balls?"
]

# Select a random rotating message at the start of the game
rotating_message = random.choice(rotating_messages)

while running:
    if not in_game and not game_over:
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100:
                    if HEIGHT // 2 <= mouse_y <= HEIGHT // 2 + 50:
                        in_game = True
                    elif HEIGHT // 2 + 60 <= mouse_y <= HEIGHT // 2 + 110:
                        running = False
    elif game_over:
        draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100:
                    if HEIGHT // 2 <= mouse_y <= HEIGHT // 2 + 50:
                        in_game = True
                        game_over = False
                        player_world_pos = pygame.Vector2(dom_world_pos[0] + 250, dom_world_pos[1])
                        current_time = start_time
                        tasks_completed = [False]
                    elif HEIGHT // 2 + 60 <= mouse_y <= HEIGHT // 2 + 110:
                        running = False
    else:
        delta_time = clock.tick(FPS) / 1000.0  # Time elapsed since the last frame in seconds
        time_elapsed_since_last_action += delta_time
        time_elapsed_for_clock_update += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Save the previous player position
        prev_player_pos = player_world_pos.copy()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_world_pos.x -= player_speed
            left, right, up, down, facing_right, facing_up, facing_down = True, False, False, False, False, False, False
        elif keys[pygame.K_RIGHT]:
            player_world_pos.x += player_speed
            left, right, up, down, facing_right, facing_up, facing_down = False, True, False, False, True, False, False
        elif keys[pygame.K_UP]:
            player_world_pos.y -= player_speed
            left, right, up, down, facing_right, facing_up, facing_down = False, False, True, False, False, True, False
        elif keys[pygame.K_DOWN]:
            player_world_pos.y += player_speed
            left, right, up, down, facing_right, facing_up, facing_down = False, False, False, True, False, False, True
        else:
            left, right, up, down = False, False, False, False

        if left or right or up or down:
            is_step = not is_step
        else:
            is_step = False

        # Set current image based on movement direction and step
        if left:
            current_image = step_left if is_step else standing_left
        elif right:
            current_image = step_right if is_step else standing_right
        elif up:
            current_image = step_up1 if is_step else standing_up
        elif down:
            current_image = step_down1 if is_step else standing_down
        else:
            current_image = standing_right if facing_right else standing_left if left else standing_up if facing_up else standing_down

        player_rect = current_image.get_rect(topleft=player_world_pos - camera_pos)

        # Check for collisions with trawka
        if not check_collisions(player_rect, trawka_rects):
            player_world_pos = prev_player_pos

        # Check for enemy collision
        if player_rect.colliderect(enemy_image.get_rect(topleft=enemy_world_pos - camera_pos)):
            game_over = True
            in_game = False

        # Camera position update
        camera_pos.update(player_world_pos.x - WIDTH // 2, player_world_pos.y - HEIGHT // 2)

        # Enemy movement
        if enemy_active:
            direction = player_world_pos - enemy_world_pos
            distance = direction.length()
            if distance > 0:
                direction.normalize_ip()
                enemy_world_pos += direction * enemy_speed

        # Draw everything
        WIN.fill(DARK_GREEN)

        # Draw map elements (house, trawka)
        for pos in trawka_positions:
            WIN.blit(trawka, pos - camera_pos)
        for pos in kamper_positions:
            WIN.blit(additional_kamper, pos - camera_pos)

        WIN.blit(dom, dom_world_pos - camera_pos)

        # Draw player and enemy
        WIN.blit(current_image, player_world_pos - camera_pos)
        WIN.blit(enemy_image, enemy_world_pos - camera_pos)

        # Update the clock
        if time_elapsed_for_clock_update >= 1:
            current_time += timedelta(minutes=1)
            time_elapsed_for_clock_update = 0
            if current_time >= end_time:
                current_time = end_time

        # Draw the clock and tasks
        draw_text(current_time.strftime("%I:%M %p"), font, WHITE, WIN, 10, 10)
        draw_tasks(tasks, tasks_completed, font, WHITE, WIN, 10, 50)

        pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
