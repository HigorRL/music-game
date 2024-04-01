import pygame
import os
from pygame.locals import *
from sys import exit

# Configurações de Janla
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Configurações do pygame
pygame.init()

# Dimensões da tela
WIDTH = 1280
HEIGHT = 720

# Cores
WHITE = (255, 255, 255)

# Configurações do jogo
FPS = 60

# Configurações do menu
menu_options = ["NOVO JOGO", "CARREGAR JOGO", "CONFIGURAÇÕES", "SOBRE", "SAIR"]
selected_option = 0

# Configurações do menu config
config_options = ["AJUSTAR VOLUME", "ALTERAR RESOLUÇÃO", "VOLTAR"]


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

# Carrega a imagem de fundo do menu de config
config_background = pygame.image.load(
    'resources/images/configuration-menu-background-v1.0.png').convert()
config_background = pygame.transform.scale(config_background, (WIDTH, HEIGHT))

# Função para desenhar o menu


def draw_menu():
    # Adiciona a imagem de fundo do menu principal
    screen.blit(menu_background, (0, 0))
    font = pygame.font.Font('resources/fonts/barcadenobar.ttf', 35)
    spacing = 44
    menu_height = len(menu_options) * spacing

    if WIDTH == 1920 and HEIGHT == 1080:
        menu_top = (HEIGHT - (menu_height + 110))
    else:
        menu_top = (HEIGHT - (menu_height + 65))
    for i, option in enumerate(menu_options):
        text = font.render(option, True, WHITE if i ==
                           selected_option else (80, 80, 80))
        # Centraliza o texto na tela
        text_rect = text.get_rect(center=(WIDTH / 2, menu_top + i * spacing))
        screen.blit(text, text_rect)

# Função para desenhar o menu de configuração


def draw_settings_menu(selected_option):
    # Adiciona a imagem de fundo do menu config
    screen.blit(config_background, (0, 0))
    font = pygame.font.Font('resources/fonts/barcadenobar.ttf', 35)
    spacing = 44
    menu_height = len(config_options) * spacing
    menu_top = (HEIGHT - menu_height) // 2
    for i, option in enumerate(config_options):
        text = font.render(option, True, WHITE if i ==
                           selected_option else (80, 80, 80))
        # Centraliza o texto na tela
        text_rect = text.get_rect(center=(WIDTH / 2, menu_top + i * spacing))
        screen.blit(text, text_rect)

# Função para o menu de configurações


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
                    selected_option = (selected_option +
                                       1) % len(config_options)
                elif event.key == K_UP or event.key == K_w:
                    selected_option = (selected_option -
                                       1) % len(config_options)
                elif event.key == K_RETURN:
                    if selected_option == 0:  # Ajustar o volume
                        adjust_volume()
                    elif selected_option == 1:  # Alterar resolução
                        change_resolution()
                    elif selected_option == 2:  # Volta para o menu principal
                        return

# Função para alterar a resolução


def change_resolution():
    global WIDTH, HEIGHT, screen, menu_background, config_background
    resolutions = [(800, 600), (1024, 768), (1280, 720),
                   (1366, 768), (1920, 1080)]
    resolution_index = 0
    while True:
        screen.blit(config_background, (0, 0))
        font = pygame.font.Font(
            'resources/fonts/barcadenobar.ttf', 35)
        spacing = 44
        menu_height = len(resolutions) * spacing
        menu_top = (HEIGHT - menu_height) / 2
        for i, res in enumerate(resolutions):
            text = font.render(
                f"{res[0]}x{res[1]}", True, WHITE if i == resolution_index else (80, 80, 80))
            text_rect = text.get_rect(
                center=(WIDTH / 2, menu_top + i * spacing))
            screen.blit(text, text_rect)
        pygame.display.update()

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
                    # Atualiza a resolução
                    WIDTH, HEIGHT = resolutions[resolution_index]
                    screen = pygame.display.set_mode(
                        (WIDTH, HEIGHT), pygame.RESIZABLE)

                    # Redimensiona as imagens de fundo
                    menu_background = pygame.transform.scale(pygame.image.load(
                        'resources/images/the-music-saga-v1.0.png'), (WIDTH, HEIGHT))
                    config_background = pygame.transform.scale(pygame.image.load(
                        'resources/images/configuration-menu-background-v1.0.png'), (WIDTH, HEIGHT))

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

        draw_volume_icon(music_volume)
        pygame.display.update()


# Função para desenhar o ícone do volume
def draw_volume_icon(volume):
    font = pygame.font.Font('resources/fonts/barcadenobar.ttf', 20)
    volume_text = font.render("VOLUME", True, WHITE)
    screen.blit(volume_text, (20, 20))  # Posição do texto do volume

    # Desenha o retângulo de fundo para o volume máximo
    background_volume_rect = pygame.Rect(
        20, 50, 20, 100)  # Retângulo do volume máximo
    # Desenha o retângulo de fundo com cor mais escura
    pygame.draw.rect(screen, (80, 80, 80), background_volume_rect)

    volume_height = int(100 * volume)

    # Desenha o ícone do volume atual como um retângulo
    # Posição e tamanho do retângulo atual baseado no volume
    volume_rect = pygame.Rect(
        20, 50 + (100 - volume_height), 20, volume_height)
    # Desenha o retângulo do volume atual
    pygame.draw.rect(screen, WHITE, volume_rect)

    # Desenha a linha de contorno para o volume máximo
    # Desenha a linha de contorno do retângulo de fundo
    pygame.draw.rect(screen, WHITE, background_volume_rect, 2)


def calculate_font_size():
    if WIDTH >= 1920:
        return 35
    elif WIDTH >= 1280:
        return 25
    else:
        return 15


def handle_about_screen():
    about_text = [
        "The Music Saga é um jogo desenvolvido para servir como projeto de",
        "conclusão do curso de Engenharia de Computação da universidade UniSatc",
        "no primeiro semestre letivo do ano de 2024. O objetivo do jogo é",
        "proporcionar entretenimento enquanto serve como um recurso educacional",
        "para aqueles interessados em aprender mais sobre música e teoria musical.",
        "",
        "Pressione ESC para voltar ao menu principal."
    ]

    while True:
        # Você pode mudar o fundo se quiser
        screen.blit(config_background, (0, 0))

        font_size = calculate_font_size()
        font = pygame.font.Font(
            'resources/fonts/barcadenobar.ttf', font_size)
        spacing = int(font_size * 0.8)
        start_y = (HEIGHT - len(about_text) * spacing) // 2

        for i, line in enumerate(about_text):
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(
                center=(WIDTH // 2, start_y + i * spacing))
            screen.blit(text, text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
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
                elif selected_option == 3:  # Seleciona sobre
                    handle_about_screen()

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
