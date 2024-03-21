import pygame
from pygame.locals import *
from sys import exit

# Configurações do pygame
pygame.init()

# Dimensões da tela
WIDTH = 1280
HEIGHT = 720

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações do jogo
FPS = 60

# Configurações do menu
menu_options = ["NOVO JOGO", "CARREGAR JOGO", "CONFIGURAÇÕES", "SOBRE", "SAIR"]
selected_option = 0

# Config de volume da música
music_volume = 0.1
volume_increment = 0.1

# Inicia a música de fundo do menu
pygame.mixer.music.load('resources/sounds/Skyfall.mp3')
pygame.mixer.music.set_volume(music_volume)
pygame.mixer.music.play(-1)

# Cria a janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The Music Saga')

# Carrega a imagem de fundo do menu
menu_background = pygame.image.load(
    'resources/images/the-music-saga-v1.0.png').convert()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# Função para desenhar o menu


def draw_menu():
    screen.blit(menu_background, (0, 0))  # Desenha o fundo do menu
    font = pygame.font.SysFont('arial', 35, bold=True)
    spacing = 44
    menu_height = len(menu_options) * spacing
    menu_top = (HEIGHT - (menu_height + 65))
    for i, option in enumerate(menu_options):
        text = font.render(option, True, WHITE if i ==
                           selected_option else (80, 80, 80))
        # Centraliza o texto na tela
        text_rect = text.get_rect(center=(WIDTH / 2, menu_top + i * spacing))
        screen.blit(text, text_rect)

# Função para desenhar o menu de configuração


def draw_settings_menu(selected_option):
    screen.fill(BLACK)  # Limpa a tela com fundo preto
    font = pygame.font.SysFont('arial', 35, bold=True)
    options = ["AJUSTAR VOLUME", "ALTERAR RESOLUÇÃO", "VOLTAR"]
    spacing = 44
    menu_height = len(options) * spacing
    menu_top = (HEIGHT - (menu_height + 65))
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE if i ==
                           selected_option else (80, 80, 80))
        # Centraliza o texto na tela
        text_rect = text.get_rect(center=(WIDTH / 2, menu_top + i * spacing))
        screen.blit(text, text_rect)

# Função para lidar com o menu de configurações


def handle_settings_menu():
    global selected_option, WIDTH, HEIGHT
    selected_option = 0
    while True:
        draw_settings_menu(selected_option)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_DOWN or event.key == K_s:
                    selected_option = (selected_option + 1) % 2
                elif event.key == K_UP or event.key == K_w:
                    selected_option = (selected_option - 1) % 2
                elif event.key == K_RETURN:
                    if selected_option == 0:  # Ajustar o volume
                        adjust_volume()
                    elif selected_option == 1:  # Alterar resolução
                        change_resolution()
                    elif selected_option == 2:  # Volta para o menu principal
                        return

# Função para alterar a resolução


def change_resolution():
    global WIDTH, HEIGHT, screen, menu_background
    resolutions = [(800, 600), (1024, 768), (1280, 720),
                   (1366, 768), (1920, 1080)]
    resolution_index = 0
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont('arial', 35, bold=True)
        spacing = 44
        menu_height = len(resolutions) * spacing
        menu_top = (HEIGHT - (menu_height + 65))
        for i, res in enumerate(resolutions):
            text = font.render(
                f"{res[0]}x{res[1]}", True, WHITE if i == resolution_index else (80, 80, 80))
            # Centraliza o texto na tela
            text_rect = text.get_rect(
                center=(WIDTH / 2, menu_top + i * spacing))
            screen.blit(text, text_rect)
        pygame.display.update()

        # Trata os eventos do teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_DOWN:
                    resolution_index = (
                        resolution_index + 1) % len(resolutions)
                elif event.key == K_UP:
                    resolution_index = (
                        resolution_index - 1) % len(resolutions)
                elif event.key == K_RETURN:
                    # Altera a resolução
                    old_width, old_height = WIDTH, HEIGHT
                    WIDTH, HEIGHT = resolutions[resolution_index]

                    # Redimensiona a imagem de fundo
                    menu_background = pygame.transform.scale(
                        menu_background, (WIDTH, HEIGHT))

                    # Atualiza a posição dos elementos na tela
                    menu_top = (HEIGHT - (menu_height + 65))
                    for i, _ in enumerate(resolutions):
                        text_rect.center = (WIDTH / 2, menu_top + i * spacing)

                    # Atualiza a janela com a nova resolução
                    pygame.display.set_mode(
                        (WIDTH, HEIGHT), pygame.RESIZABLE)
                    pygame.display.set_caption('The Music Saga')

                    return

# Função para ajustar o volume


def adjust_volume():
    global music_volume
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_UP:  # Aumentar o volume
                    music_volume = min(1, music_volume + volume_increment)
                    pygame.mixer.music.set_volume(music_volume)
                elif event.key == K_DOWN:  # Diminuir o volume
                    music_volume = max(0, music_volume - volume_increment)
                    pygame.mixer.music.set_volume(music_volume)
                elif event.key == K_RETURN:  # Voltar ao menu de configurações
                    return

# Função para lidar com os eventos


def handle_events():
    global selected_option
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_DOWN or event.key == K_s:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == K_UP or event.key == K_w:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == K_RETURN:
                if selected_option == len(menu_options) - 1:
                    pygame.quit()
                    exit()
                elif selected_option == 2:  # Seleciona configurações
                    handle_settings_menu()

# Loop principal do jogo


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        handle_events()
        draw_menu()
        pygame.display.update()


# Inicia o jogo
if __name__ == "__main__":
    main()
