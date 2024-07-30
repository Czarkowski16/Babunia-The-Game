import pygame
import sys
import random
from datetime import datetime, timedelta

# Inicjalizacja Pygame
pygame.init()

FPS = 60
WIDTH, HEIGHT = 1220, 720
MAP_WIDTH, MAP_HEIGHT = 6000, 6000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babunia")

# Ładowanie obrazów
trawka = pygame.transform.scale(pygame.image.load("trawka.png"), (100, 100))
dom = pygame.transform.scale(pygame.image.load('dom.png'), (200, 200))
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
enemy_image = pygame.transform.scale(pygame.image.load("babunia.png"), (200, 200))
additional_trawka = pygame.transform.scale(pygame.image.load("drzewo.png"), (100, 100))
additional_kamper = pygame.transform.scale(pygame.image.load("kamper.png"), (200, 200))

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_tasks(tasks, tasks_completed, font, color, surface, x, y):
    for i, task in enumerate(tasks):
        task_text = f"{'[X]' if tasks_completed[i] else '[ ]'} {task}"
        draw_text(task_text, font, color, surface, x, y + i * 30)

def check_collisions(rect, obstacles):
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            return True
    return False

def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, WHITE, surface, x + 10, y + 10)
    return pygame.Rect(x, y, width, height)

def main():
    player_world_pos = pygame.Vector2(MAP_WIDTH // 2, MAP_HEIGHT // 2)
    enemy_world_pos = pygame.Vector2(300, 300)
    dom_world_pos = (1000, 1000)
    dom_rect = dom.get_rect(topleft=dom_world_pos)

    num_trawka = 17
    trawka_positions = [(random.randint(0, MAP_WIDTH - 100), random.randint(0, MAP_HEIGHT - 100)) for _ in range(num_trawka)]
    trawka_rects = [additional_trawka.get_rect(topleft=pos) for pos in trawka_positions]

    num_kamper = 1
    kamper_positions = [(random.randint(0, MAP_WIDTH - 100), random.randint(0, MAP_HEIGHT - 100)) for _ in range(num_kamper)]
    kamper_rects = [additional_kamper.get_rect(topleft=pos) for pos in kamper_positions]

    left, right, down, up, is_step, facing_right, facing_down, facing_up = False, False, False, False, False, True, False, False
    player_speed = 4
    enemy_speed = 6

    camera_pos = pygame.Vector2(player_world_pos.x - WIDTH // 2, player_world_pos.y - HEIGHT // 2)

    start_time = datetime.strptime("08:00 AM", "%I:%M %p")
    end_time = datetime.strptime("12:00 PM", "%I:%M %p")
    current_time = start_time

    tasks = ["Idź na kebsa"]
    tasks_completed = [False]

    running = True
    clock = pygame.time.Clock()
    time_elapsed_since_last_action = 0
    time_elapsed_for_clock_update = 0
    down_step_index = 0
    up_step_index = 0

    enemy_active = False
    game_over = False

    while running:
        delta_time = clock.tick(FPS) / 1000.0
        time_elapsed_since_last_action += delta_time
        time_elapsed_for_clock_update += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    main()
                if quit_button.collidepoint(mouse_pos):
                    running = False

        if game_over:
            WIN.fill(WHITE)
            draw_text("Game Over", big_font, BLACK, WIN, WIDTH // 2 - 150, HEIGHT // 2 - 100)
            restart_button = draw_button("Restart", font, BLACK, WIN, WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
            quit_button = draw_button("Quit", font, BLACK, WIN, WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
            pygame.display.update()
            continue

        prev_player_pos = player_world_pos.copy()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_world_pos.x -= player_speed
            left, right, down, up, facing_right, facing_down, facing_up = True, False, False, False, False, False, False
            if time_elapsed_since_last_action > 0.1:
                is_step = not is_step
                time_elapsed_since_last_action = 0
        elif keys[pygame.K_RIGHT]:
            player_world_pos.x += player_speed
            left, right, down, up, facing_right, facing_down, facing_up = False, True, False, False, True, False, False
            if time_elapsed_since_last_action > 0.1:
                is_step = not is_step
                time_elapsed_since_last_action = 0
        elif keys[pygame.K_DOWN]:
            player_world_pos.y += player_speed
            left, right, down, up, facing_right, facing_down, facing_up = False, False, True, False, False, True, False
            if time_elapsed_since_last_action > 0.1:
                down_step_index = (down_step_index + 1) % 4
                time_elapsed_since_last_action = 0
        elif keys[pygame.K_UP]:
            player_world_pos.y -= player_speed
            left, right, down, up, facing_right, facing_down, facing_up = False, False, False, True, False, False, True
            if time_elapsed_since_last_action > 0.1:
                up_step_index = (up_step_index + 1) % 4
                time_elapsed_since_last_action = 0
        else:
            left, right, down, up = False, False, False, False

        current_image = None
        if left and is_step:
            current_image = step_left
        elif left:
            current_image = standing_left
        elif right and is_step:
            current_image = step_right
        elif right:
            current_image = standing_right
        elif down:
            if down_step_index == 0:
                current_image = standing_down
            elif down_step_index == 1:
                current_image = step_down1
            elif down_step_index == 2:
                current_image = standing_down
            elif down_step_index == 3:
                current_image = step_down2
        elif up:
            if up_step_index == 0:
                current_image = standing_up
            elif up_step_index == 1:
                current_image = step_up1
            elif up_step_index == 2:
                current_image = standing_up
            elif up_step_index == 3:
                current_image = step_up2

        if current_image is None:
            current_image = standing_right

        player_rect = current_image.get_rect(topleft=player_world_pos)

        if check_collisions(player_rect, [dom_rect] + trawka_rects + kamper_rects):
            player_world_pos = prev_player_pos

        if current_time >= datetime.strptime("11:00 AM", "%I:%M %p"):
            enemy_active = True

        if enemy_active:
            if enemy_world_pos.x < player_world_pos.x:
                enemy_world_pos.x += enemy_speed
            elif enemy_world_pos.x > player_world_pos.x:
                enemy_world_pos.x -= enemy_speed
            if enemy_world_pos.y < player_world_pos.y:
                enemy_world_pos.y += enemy_speed
            elif enemy_world_pos.y > player_world_pos.y:
                enemy_world_pos.y -= enemy_speed

            if player_rect.colliderect(enemy_image.get_rect(topleft=enemy_world_pos)):
                game_over = True
                continue

        for i, kamper_pos in enumerate(kamper_positions):
            kamper_rect = additional_kamper.get_rect(topleft=kamper_pos)
            if player_rect.colliderect(kamper_rect) and not tasks_completed[i]:
                tasks_completed[i] = True

        if player_rect.colliderect(dom_rect) and all(tasks_completed):
            enemy_active = False
            enemy_world_pos = pygame.Vector2(300, 300)
            current_time = start_time
            tasks_completed = [False]

        camera_pos.x = player_world_pos.x - WIDTH // 2
        camera_pos.y = player_world_pos.y - HEIGHT // 2

        if time_elapsed_for_clock_update >= 1:
            current_time += timedelta(minutes=1)
            if current_time >= end_time:
                current_time = start_time
            time_elapsed_for_clock_update = 0

        WIN.fill(WHITE)

        for x in range(0, MAP_WIDTH, trawka.get_width()):
            for y in range(0, MAP_HEIGHT, trawka.get_height()):
                WIN.blit(trawka, (x - camera_pos.x, y - camera_pos.y))

        for pos in trawka_positions:
            WIN.blit(additional_trawka, (pos[0] - camera_pos.x, pos[1] - camera_pos.y))

        for pos in kamper_positions:
            WIN.blit(additional_kamper, (pos[0] - camera_pos.x, pos[1] - camera_pos.y))

        WIN.blit(dom, (dom_world_pos[0] - camera_pos.x, dom_world_pos[1] - camera_pos.y))

        WIN.blit(current_image, (player_world_pos.x - camera_pos.x, player_world_pos.y - camera_pos.y))

        if enemy_active:
            WIN.blit(enemy_image, (enemy_world_pos.x - camera_pos.x, enemy_world_pos.y - camera_pos.y))

        time_str = current_time.strftime("%I:%M %p")
        draw_text(f"Czas: {time_str}", font, BLACK, WIN, 10, 10)

        draw_tasks(tasks, tasks_completed, font, BLACK, WIN, WIDTH - 300, 10)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
