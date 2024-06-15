import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 1220, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babunia")

# Kolory
WHITE = (255, 255, 255)

# Ładowanie sprite'ów gracza
standing_right = pygame.image.load("PanPole.png")
step_right = pygame.image.load("2.png")
standing_left = pygame.image.load("3.png")
step_left = pygame.image.load("4.png")

# Skalowanie obrazów
standing_right = pygame.transform.scale(standing_right, (200, 200))
step_right = pygame.transform.scale(step_right, (200, 200))
standing_left = pygame.transform.scale(standing_left, (200, 200))
step_left = pygame.transform.scale(step_left, (200, 200))

# Ustawienie początkowej pozycji gracza
player_rect = standing_right.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)

# Zmienne animacji
left = False
right = False
is_step = False
facing_right = True
player_speed = 8

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

    # Aktualizacja okna gry
    WIN.fill(WHITE)

    if left:
        current_image = step_left if is_step else standing_left
    elif right:
        current_image = step_right if is_step else standing_right
    else:
        current_image = standing_right if facing_right else standing_left

    WIN.blit(current_image, player_rect)

    pygame.display.update()

    # Opóźnienie
    pygame.time.delay(100)

# Zakończenie Pygame
pygame.quit()
sys.exit()