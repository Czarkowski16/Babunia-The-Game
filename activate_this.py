import pygame
import sys
import random
from datetime import datetime, timedelta

# Inicjalizacja Pygame
pygame.init()

FPS = 60  # Liczba klatek na sekundę
WIDTH, HEIGHT = 1220, 720  # Ustawienia okna gry
MAP_WIDTH, MAP_HEIGHT = 3000, 3000  # Ustawienia mapy (większa niż okno gry)

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babunia")

# Ładowanie obrazów
trawka = pygame.transform.scale(pygame.image.load("trawka.png"), (100, 100))
dom = pygame.transform.scale(pygame.image.load('dom.png'), (400, 400))
dom_world_pos = (1000, 1000)
dom_rect = dom.get_rect(topleft=dom_world_pos)

standing_right = pygame.transform.scale(pygame.image.load("PanPole.png"), (200, 200))
step_right = pygame.transform.scale(pygame.image.load("2.png"), (200, 200))
standing_left = pygame.transform.scale(pygame.image.load("3.png"), (200, 200))
step_left = pygame.transform.scale(pygame.image.load("5.png"), (200, 200))

# Ustawienie początkowej pozycji gracza w świecie
player_world_pos = pygame.Vector2(MAP_WIDTH // 2, MAP_HEIGHT // 2)

# Ładowanie sprite'a przeciwnika
enemy_image = pygame.transform.scale(pygame.image.load("babunia.png"), (200, 200))

# Ustawienie początkowej pozycji przeciwnika
enemy_world_pos = pygame.Vector2(300, 300)

# Tworzenie listy losowych pozycji dla dodatkowej trawy
num_trawka = 17
trawka_positions = [(random.randint(0, MAP_WIDTH - 100), random.randint(0, MAP_HEIGHT - 100)) for _ in range(num_trawka)]
additional_trawka = pygame.transform.scale(pygame.image.load("drzewo.png"), (100, 100))
trawka_rects = [additional_trawka.get_rect(topleft=pos) for pos in trawka_positions]

# Tworzenie listy losowych pozycji dla kamperów
num_kamper = 1
kamper_positions = [(random.randint(0, MAP_WIDTH - 100), random.randint(0, MAP_HEIGHT - 100)) for _ in range(num_kamper)]
additional_kamper = pygame.transform.scale(pygame.image.load("kamper.png"), (200, 200))
kamper_rects = [additional_kamper.get_rect(topleft=pos) for pos in kamper_positions]

# Zmienne animacji
left, right, is_step, facing_right = False, False, False, True
player_speed = 7  # Prędkość gracza
enemy_speed = 1

# Kamera
camera_pos = pygame.Vector2(player_world_pos.x - WIDTH // 2, player_world_pos.y - HEIGHT // 2)

# Ustawienia zegara
start_time = datetime.strptime("08:00 AM", "%I:%M %p")
end_time = datetime.strptime("12:00 PM", "%I:%M %p")
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

# Zmienna dla przeciwnika
enemy_active = False

# Funkcja sprawdzająca kolizje gracza z przeszkodami
def check_collisions(rect, obstacles):
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            return True
    return False

while running:
    delta_time = clock.tick(FPS) / 1000.0  # Czas, który minął od ostatniej klatki, w sekundach
    time_elapsed_since_last_action += delta_time
    time_elapsed_for_clock_update += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zapisanie poprzedniej pozycji gracza
    prev_player_pos = player_world_pos.copy()

    # Ruch gracza
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_world_pos.x -= player_speed
        left, right, facing_right = True, False, False
        if time_elapsed_since_last_action > 0.1:
            is_step = not is_step  # Zmieniaj obrazek kroku
            time_elapsed_since_last_action = 0
    elif keys[pygame.K_RIGHT]:
        player_world_pos.x += player_speed
        left, right, facing_right = False, True, True
        if time_elapsed_since_last_action > 0.1:
            is_step = not is_step  # Zmieniaj obrazek kroku
            time_elapsed_since_last_action = 0
    else:
        left, right = False, False

    if keys[pygame.K_UP]:
        player_world_pos.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_world_pos.y += player_speed

    # Aktualizacja prostokąta gracza po ruchu
    current_image = step_left if left and is_step else step_right if right and is_step else standing_left if not facing_right else standing_right
    player_rect = current_image.get_rect(topleft=player_world_pos)

    # Sprawdzanie kolizji gracza z domem, drzewami i kamperami
    if check_collisions(player_rect, [dom_rect] + trawka_rects + kamper_rects):
        player_world_pos = prev_player_pos  # Przywrócenie poprzedniej pozycji gracza w przypadku kolizji

    # Aktywacja przeciwnika po 11:00 AM
    if current_time >= datetime.strptime("11:00 AM", "%I:%M %p"):
        enemy_active = True

    # Ruch przeciwnika - goni gracza
    if enemy_active:
        if enemy_world_pos.x < player_world_pos.x:
            enemy_world_pos.x += enemy_speed
        elif enemy_world_pos.x > player_world_pos.x:
            enemy_world_pos.x -= enemy_speed
        if enemy_world_pos.y < player_world_pos.y:
            enemy_world_pos.y += enemy_speed
        elif enemy_world_pos.y > player_world_pos.y:
            enemy_world_pos.y -= enemy_speed

        # Kolizja z przeciwnikiem
        if player_rect.colliderect(enemy_image.get_rect(topleft=enemy_world_pos)):
            enemy_active = False
            enemy_world_pos = pygame.Vector2(300, 300)
            current_time = start_time

    # Sprawdzenie, czy gracz dotarł do domu
    if player_rect.colliderect(dom_rect):
        if enemy_active:
            enemy_active = False
            enemy_world_pos = pygame.Vector2(300, 300)
            current_time = start_time

    # Aktualizacja pozycji kamery
    camera_pos.x = player_world_pos.x - WIDTH // 2
    camera_pos.y = player_world_pos.y - HEIGHT // 2

    # Aktualizacja czasu
    if time_elapsed_for_clock_update >= 1:
        current_time += timedelta(minutes=1)
        if current_time >= end_time:
            current_time = start_time
        time_elapsed_for_clock_update = 0

    # Rysowanie na ekranie
    WIN.fill(WHITE)  # Wypełnienie ekranu białym kolorem

    # Rysowanie trawy jako tło
    for x in range(0, MAP_WIDTH, trawka.get_width()):
        for y in range(0, MAP_HEIGHT, trawka.get_height()):
            WIN.blit(trawka, (x - camera_pos.x, y - camera_pos.y))

    # Rysowanie losowo porozmieszczonej trawy
    for pos in trawka_positions:
        WIN.blit(additional_trawka, (pos[0] - camera_pos.x, pos[1] - camera_pos.y))

    # Rysowanie kamperów
    for pos in kamper_positions:
        WIN.blit(additional_kamper, (pos[0] - camera_pos.x, pos[1] - camera_pos.y))

    # Rysowanie domu
    WIN.blit(dom, (dom_world_pos[0] - camera_pos.x, dom_world_pos[1] - camera_pos.y))

    # Rysowanie gracza
    WIN.blit(current_image, (player_world_pos.x - camera_pos.x, player_world_pos.y - camera_pos.y))

    # Rysowanie przeciwnika
    if enemy_active:
        WIN.blit(enemy_image, (enemy_world_pos.x - camera_pos.x, enemy_world_pos.y - camera_pos.y))

    # Rysowanie zegara
    time_str = current_time.strftime("%I:%M %p")
    draw_text(f"Czas: {time_str}", font, BLACK, WIN, 10, 10)

    pygame.display.update()

# Zakończenie Pygame
pygame.quit()
sys.exit()
