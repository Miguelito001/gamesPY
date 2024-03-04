import pygame
import random
import math
from pygame.locals import *

# Inicialização do Pygame
pygame.init()

# Definições de tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meu Jogo FPS")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Variáveis do jogador
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Variáveis dos inimigos
enemies = []
enemy_speed = 3
enemy_spawn_rate = 100
enemy_spawn_counter = 0

# Variáveis dos tiros
bullets = []
bullet_speed = 8

# Pontuação
score = 0
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Loop principal do jogo
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Input do jogador
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.atan2(mouse_y - player_y, mouse_x - player_x)

    if keys[K_w]:
        player_y -= player_speed
    if keys[K_s]:
        player_y += player_speed
    if keys[K_a]:
        player_x -= player_speed
    if keys[K_d]:
        player_x += player_speed

    # Limitar movimento do jogador dentro da tela
    player_x = max(0, min(WIDTH - 20, player_x))
    player_y = max(0, min(HEIGHT - 20, player_y))

    # Spawn de inimigos
    if enemy_spawn_counter <= 0:
        enemy_x = random.randint(0, WIDTH - 20)
        enemy_y = random.randint(0, HEIGHT - 20)
        enemies.append([enemy_x, enemy_y])
        enemy_spawn_counter = enemy_spawn_rate
    else:
        enemy_spawn_counter -= 1

    # Mover inimigos em direção ao jogador
    for enemy in enemies:
        if enemy[0] < player_x:
            enemy[0] += enemy_speed
        elif enemy[0] > player_x:
            enemy[0] -= enemy_speed

        if enemy[1] < player_y:
            enemy[1] += enemy_speed
        elif enemy[1] > player_y:
            enemy[1] -= enemy_speed

        # Detectar colisões entre o jogador e os inimigos
        if player_x < enemy[0] + 20 and player_x + 20 > enemy[0] and player_y < enemy[1] + 20 and player_y + 20 > enemy[1]:
            score -= 1
            enemies.remove(enemy)

    # Disparar tiros
    if pygame.mouse.get_pressed()[0]:
        bullets.append([player_x + 10, player_y + 10, angle])

    # Mover tiros
    for bullet in bullets:
        bullet[0] += bullet_speed * math.cos(bullet[2])
        bullet[1] += bullet_speed * math.sin(bullet[2])
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets.remove(bullet)

    # Detectar colisões entre tiros e inimigos
    for bullet in bullets:
        for enemy in enemies:
            if enemy[0] < bullet[0] < enemy[0] + 20 and enemy[1] < bullet[1] < enemy[1] + 20:
                score += 1
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Limpar a tela
    screen.fill(BLACK)

    # Desenhar o jogador
    pygame.draw.rect(screen, WHITE, (player_x, player_y, 20, 20))

    # Desenhar os inimigos
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 20, 20))

    # Desenhar os tiros
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 5, 5))

    # Desenhar a pontuação
    score_text = font.render("Pontuação: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Atualizar a tela
    pygame.display.flip()

    # Limitar a taxa de quadros
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()
