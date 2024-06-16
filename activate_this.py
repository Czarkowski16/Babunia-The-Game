import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 1220, 720
# Kolory
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babunia")

# Ładowanie obrazu tła
trawka = pygame.image.load("trawka.png")
trawka = pygame.transform.scale(trawka, (WIDTH, HEIGHT))  # Skalowanie trawy na rozmiar okna

# Ładowanie obrazu domu
dom = pygame.image.load ('dom.png')
dom = pygame.transform.scale(dom, (300, 300))  # Skalowanie domu
dom_rect = dom.get_rect()
dom_rect.topleft = (WIDTH - 350, HEIGHT - 350)  # Ustawienie pozycji domu

# Ładowanie sprite'ów gracza
standing_right = pygame.image.load("PanPole.png")
step_right = pygame.image.load("2.png")
standing_left = pygame.image.load("3.png")
step_left = pygame.image.load("5.png")

# Skalowanie obrazów Pole
standing_right = pygame.transform.scale(standing_right, (200, 200))
step_right = pygame.transform.scale(step_right, (200, 200))
standing_left = pygame.transform.scale(standing_left, (200, 200))
step_left = pygame.transform.scale(step_left, (200, 200))

# Ustawienie początkowej pozycji gracza
player_rect = standing_right.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)

# Ładowanie sprite'a przeciwnika
enemy_image = pygame.image.load("babunia.png")
enemy_image = pygame.transform.scale(enemy_image, (200, 200))

# Ustawienie początkowej pozycji przeciwnika
enemy_rect = enemy_image.get_rect()
enemy_rect.center = (WIDTH // 4, HEIGHT // 4)

# Tworzenie listy losowych pozycji dla dodatkowej trawy
num_trawka = 10  # Liczba dodatkowych traw
trawka_positions = [(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)) for _ in range(num_trawka)]
additional_trawka = pygame.image.load("trawa.png")
additional_trawka = pygame.transform.scale(additional_trawka, (100, 100))

# Zmienne animacji
left = False
right = False
is_step = False
facing_right = True
player_speed = 9
enemy_speed = 2

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ruch gracza
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        left = True
        right = False
        is_step = not is_step  # Zmieniaj obrazek kroku
        facing_right = False
    elif keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
        left = False
        right = True
        is_step = not is_step  # Zmieniaj obrazek kroku
        facing_right = True
    else:
        left = False
        right = False

    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Ruch przeciwnika - goni gracza
    if enemy_rect.x < player_rect.x:
        enemy_rect.x += enemy_speed
    elif enemy_rect.x > player_rect.x:
        enemy_rect.x -= enemy_speed

    if enemy_rect.y < player_rect.y:
        enemy_rect.y += enemy_speed
    elif enemy_rect.y > player_rect.y:
        enemy_rect.y -= enemy_speed

    # Aktualizacja okna gry
    WIN.blit(trawka, (0, 0))  # Rysowanie trawy jako tło

    # Rysowanie losowo porozmieszczonej trawy
    for pos in trawka_positions:
        WIN.blit(additional_trawka, pos)

    # Rysowanie domu
    WIN.blit(dom, dom_rect.topleft)

    # Rysowanie gracza
    if left:
        current_image = step_left if is_step else standing_left
    elif right:
        current_image = step_right if is_step else standing_right
    else:
        current_image = standing_right if facing_right else standing_left

    WIN.blit(current_image, player_rect)
    WIN.blit(enemy_image, enemy_rect)

    pygame.display.update()

    # Opóźnienie
    pygame.time.delay(100)

# Zakończenie Pygame
pygame.quit()
sys.exit()
