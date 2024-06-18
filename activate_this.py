import pygame
import sys
import random
from datetime import datetime, timedelta

# Inicjalizacja Pygame
pygame.init()

FPS = 60  # Liczba klatek na sekundę
# Ustawienia okna gry
WIDTH, HEIGHT = 1220, 720
# Ustawienia mapy (większa niż okno gry)
MAP_WIDTH, MAP_HEIGHT = 3000, 3000

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babunia")

# Ładowanie obrazów
trawka = pygame.image.load("trawka.png")
trawka = pygame.transform.scale(trawka, (100, 100))  # Skalowanie trawy

dom = pygame.image.load('dom.png')
dom = pygame.transform.scale(dom, (300, 300))  # Skalowanie domu
dom_world_pos = (1000, 1000)  # Pozycja domu w świecie

standing_right = pygame.image.load("PanPole.png")
step_right = pygame.image.load("2.png")
standing_left = pygame.image.load("3.png")
step_left = pygame.image.load("5.png")

# Skalowanie obrazów Pole
standing_right = pygame.transform.scale(standing_right, (200, 200))
step_right = pygame.transform.scale(step_right, (200, 200))
standing_left = pygame.transform.scale(standing_left, (200, 200))
step_left = pygame.transform.scale(step_left, (200, 200))

# Ustawienie początkowej pozycji gracza w świecie
player_world_pos = pygame.Vector2(MAP_WIDTH // 2, MAP_HEIGHT // 2)

# Ładowanie sprite'a przeciwnika
enemy_image = pygame.image.load("babunia.png")
enemy_image = pygame.transform.scale(enemy_image, (200, 200))

# Ustawienie początkowej pozycji przeciwnika
enemy_world_pos = pygame.Vector2(300, 300)

# Tworzenie listy losowych pozycji dla dodatkowej trawy
num_trawka = 10  # Liczba dodatkowych traw
trawka_positions = [(random.randint(0, MAP_WIDTH - 100), random.randint(0, MAP_HEIGHT - 100)) for _ in range(num_trawka)]
additional_trawka = pygame.image.load("drzewo.png")
additional_trawka = pygame.transform.scale(additional_trawka, (100, 100))

# Zmienne animacji
left = False
right = False
is_step = False
facing_right = True
player_speed = 5 # Prędkość gracza
enemy_speed = 2

# Kamera
camera_pos = pygame.Vector2(player_world_pos.x - WIDTH // 2, player_world_pos.y - HEIGHT // 2)

# Ustawienia zegara
start_time = datetime.strptime("08:00 AM", "%I:%M %p")
end_time = datetime.strptime("12:00 PM", "%I:%M %p")  # Zmiana na 12 PM
current_time = start_time

# Czcionka dla zegara
font = pygame.font.Font(None, 36)

# Funkcja do rysowania tekstu na ekranie
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Główna pętla gry
running = True
clock = pygame.time.Clock()
time_elapsed_since_last_action = 0
time_elapsed_for_clock_update = 0

while running:
    delta_time = clock.tick(FPS) / 1000.0  # Czas, który minął od ostatniej klatki, w sekundach
    time_elapsed_since_last_action += delta_time
    time_elapsed_for_clock_update += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ruch gracza
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_world_pos.x -= player_speed
        left = True
        right = False
        if time_elapsed_since_last_action > 0.1:
            is_step = not is_step  # Zmieniaj obrazek kroku
            time_elapsed_since_last_action = 0
        facing_right = False
    elif keys[pygame.K_RIGHT]:
        player_world_pos.x += player_speed
        left = False
        right = True
        if time_elapsed_since_last_action > 0.1:
            is_step = not is_step  # Zmieniaj obrazek kroku
            time_elapsed_since_last_action = 0
        facing_right = True
    else:
        left = False
        right = False

    if keys[pygame.K_UP]:
        player_world_pos.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_world_pos.y += player_speed

    # Ruch przeciwnika - goni gracza
    if enemy_world_pos.x < player_world_pos.x:
        enemy_world_pos.x += enemy_speed
    elif enemy_world_pos.x > player_world_pos.x:
        enemy_world_pos.x -= enemy_speed

    if enemy_world_pos.y < player_world_pos.y:
        enemy_world_pos.y += enemy_speed
    elif enemy_world_pos.y > player_world_pos.y:
        enemy_world_pos.y -= enemy_speed

    # Aktualizacja pozycji kamery
    camera_pos.x = player_world_pos.x - WIDTH // 2
    camera_pos.y = player_world_pos.y - HEIGHT // 2

    # Aktualizacja czasu
    if time_elapsed_for_clock_update >= 1:
        current_time += timedelta(minutes=1)
        if current_time >= end_time:
            current_time = start_time
        time_elapsed_for_clock_update = 0

    # Debugowanie: wydrukowanie aktualnego czasu i upływu czasu
    print(f"Current Time: {current_time.strftime('%I:%M %p')}, Elapsed for Clock Update: {time_elapsed_for_clock_update}")

    # Aktualizacja okna gry
    WIN.fill(WHITE)  # Wypełnienie tła kolorem białym

    # Rysowanie trawy jako tło
    for x in range(0, MAP_WIDTH, trawka.get_width()):
        for y in range(0, MAP_HEIGHT, trawka.get_height()):
            WIN.blit(trawka, (x - camera_pos.x, y - camera_pos.y))

    # Rysowanie losowo porozmieszczonej trawy
    for pos in trawka_positions:
        pos_screen = (pos[0] - camera_pos.x, pos[1] - camera_pos.y)
        WIN.blit(additional_trawka, pos_screen)

    # Rysowanie domu
    dom_screen_pos = (dom_world_pos[0] - camera_pos.x, dom_world_pos[1] - camera_pos.y)
    WIN.blit(dom, dom_screen_pos)

    # Rysowanie gracza
    if left:
        current_image = step_left if is_step else standing_left
    elif right:
        current_image = step_right if is_step else standing_right
    else:
        current_image = standing_right if facing_right else standing_left

    player_screen_pos = (player_world_pos.x - camera_pos.x, player_world_pos.y - camera_pos.y)
    WIN.blit(current_image, player_screen_pos)

    # Rysowanie przeciwnika
    enemy_screen_pos = (enemy_world_pos.x - camera_pos.x, enemy_world_pos.y - camera_pos.y)
    WIN.blit(enemy_image, enemy_screen_pos)

    # Rysowanie zegara
    time_str = current_time.strftime("%I:%M %p")
    draw_text(f"Czas: {time_str}", font, BLACK, WIN, 10, 10)

    pygame.display.update()

# Zakończenie Pygame
pygame.quit()
sys.exit()

