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

# Ładowanie sprite'a gracza
player_image = pygame.image.load("PanPole.png")
player_rect = player_image.get_rect()
player_speed = 5
player_image = pygame.transform.scale(player_image, (300, 300))
# Ustawienie początkowej pozycji gracza
player_rect.center = (WIDTH // 2, HEIGHT // 2)

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
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Aktualizacja okna gry
    WIN.fill(WHITE)
    WIN.blit(player_image, player_rect)
    pygame.display.update()

    # Opóźnienie
    pygame.time.delay(30)

# Zakończenie Pygame
pygame.quit()
sys.exit()