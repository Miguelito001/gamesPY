import pygame
import random
import sys

# Inicializando o Pygame
pygame.init()

# Definindo as constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Corrida")

# Carregando as imagens dos carros
player_car = pygame.image.load('download.jfif')
enemy_car = pygame.image.load('download (1).jfif')

# Definindo as dimensões dos carros
car_width = 73
car_height = 125

# Função para desenhar os carros na tela
def draw_car(x, y, car):
    screen.blit(car, (x, y))

# Função principal do jogo
def game():
    # Posição inicial do carro do jogador
    player_x = (SCREEN_WIDTH - car_width) // 2
    player_y = SCREEN_HEIGHT - car_height - 20

    # Posições iniciais dos carros inimigos
    enemy_x = random.randint(0, SCREEN_WIDTH - car_width)
    enemy_y = -600
    enemy_speed = 1

    # Velocidade do carro do jogador
    player_speed = 0

    # Loop principal do jogo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controlando o movimento do carro do jogador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed = -2
                if event.key == pygame.K_RIGHT:
                    player_speed = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed = 0

        # Atualizando a posição do carro do jogador
        player_x += player_speed

        # Limitando o movimento do carro do jogador dentro da tela
        if player_x < 0:
            player_x = 0
        elif player_x > SCREEN_WIDTH - car_width:
            player_x = SCREEN_WIDTH - car_width

        # Atualizando a posição do carro inimigo
        enemy_y += enemy_speed

        # Verificando colisões
        if player_y < enemy_y + car_height:
            if player_x < enemy_x + car_width and player_x + car_width > enemy_x:
                crash()

        # Redesenhando a tela
        screen.fill(WHITE)
        draw_car(player_x, player_y, player_car)
        draw_car(enemy_x, enemy_y, enemy_car)

        # Se o carro inimigo sair da tela, reposicioná-lo
        if enemy_y > SCREEN_HEIGHT:
            enemy_y = 0 - car_height
            enemy_x = random.randint(0, SCREEN_WIDTH - car_width)

        pygame.display.update()

# Função para mostrar a tela de colisão
def crash():
    message_display('Você bateu!')

# Função para mostrar mensagens na tela
def message_display(text):
    font = pygame.font.Font(None, 70)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
    game()

# Iniciando o jogo
game()
