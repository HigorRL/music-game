import pygame
import os
import random
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
BLACK = (0, 0, 0)

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

# Carrega as imagens de fundo para as fases
primeiro_mundo_background = pygame.image.load(
    'resources/images/ilha-das-notas.webp').convert()
primeiro_mundo_background = pygame.transform.scale(
    primeiro_mundo_background, (WIDTH, HEIGHT))

segundo_mundo_background = pygame.image.load(
    'resources/images/floresta-do-ritmo.webp').convert()
segundo_mundo_background = pygame.transform.scale(
    segundo_mundo_background, (WIDTH, HEIGHT))

terceiro_mundo_background = pygame.image.load(
    'resources/images/vale-das-escalas.webp').convert()
terceiro_mundo_background_mundo_background = pygame.transform.scale(
    terceiro_mundo_background, (WIDTH, HEIGHT))

quarto_mundo_background = pygame.image.load(
    'resources/images/caverna-dos-intervalos.webp').convert()
quarto_mundo_background = pygame.transform.scale(
    quarto_mundo_background, (WIDTH, HEIGHT))

quinto_mundo_background = pygame.image.load(
    'resources/images/castelo-dos-acordes.webp').convert()
quinto_mundo_background = pygame.transform.scale(
    quinto_mundo_background, (WIDTH, HEIGHT))

sexto_mundo_background = pygame.image.load(
    'resources/images/torre-da-composicao.webp').convert()
sexto_mundo_background = pygame.transform.scale(
    sexto_mundo_background, (WIDTH, HEIGHT))

# Carrega os sprites
guide_sprite_image = pygame.image.load(
    'resources/sprites/guia.png').convert_alpha()
guide_sprite = pygame.transform.scale(guide_sprite_image, (250, 300))

note_sprites = {
    "do": pygame.transform.scale(pygame.image.load('resources/sprites/do.png').convert_alpha(), (100, 100)),
    "re": pygame.transform.scale(pygame.image.load('resources/sprites/re.png').convert_alpha(), (100, 100)),
    "mi": pygame.transform.scale(pygame.image.load('resources/sprites/mi.png').convert_alpha(), (100, 100)),
    "fa": pygame.transform.scale(pygame.image.load('resources/sprites/fa.png').convert_alpha(), (100, 100)),
    "sol": pygame.transform.scale(pygame.image.load('resources/sprites/sol.png').convert_alpha(), (100, 100)),
    "la": pygame.transform.scale(pygame.image.load('resources/sprites/la.png').convert_alpha(), (100, 100)),
    "si": pygame.transform.scale(pygame.image.load('resources/sprites/si.png').convert_alpha(), (100, 100)),
}

notes_found = [False] * len(note_sprites)

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


def draw_note_legend():
    legend_x = 50
    legend_y = 100
    padding = 10
    note_height = 50
    border_padding = 5  # Espaçamento adicional para a borda
    title_padding = 30  # Espaço entre o título e a primeira nota
    font = pygame.font.Font('resources/fonts/barcadenobar.ttf', 24)
    # Fonte para o "v" de verificado
    checkmark_font = pygame.font.Font('resources/fonts/barcadenobar.ttf', 30)

    # Desenha o título da legenda
    title_text = font.render("Legenda de Notas", True, WHITE)
    title_rect = title_text.get_rect()
    title_rect.topleft = (legend_x, legend_y - title_padding)
    pygame.draw.rect(screen, BLACK, (title_rect.left - border_padding, title_rect.top - border_padding,
                                     title_rect.width + 2 * border_padding, title_rect.height + 2 * border_padding))
    screen.blit(title_text, title_rect)

    for i, (note_name, sprite) in enumerate(note_sprites.items()):
        # Escala e desenha o sprite da nota
        resized_sprite = pygame.transform.scale(
            sprite, (note_height, note_height))
        sprite_x = legend_x
        sprite_y = legend_y + i * (note_height + padding)
        screen.blit(resized_sprite, (sprite_x, sprite_y))

        # Renderiza e desenha o texto da nota
        note_text = font.render(note_name.capitalize(), True, BLACK)
        text_x = legend_x + note_height + padding
        text_y = sprite_y
        screen.blit(note_text, (text_x, text_y))

        # Verifica se a nota foi encontrada e desenha um "v" verde ao lado
        if notes_found[i]:
            checkmark = checkmark_font.render(
                "✓", True, (0, 255, 0))  # Cor verde para o "v"
            # Posiciona o "v" um pouco à direita do nome da nota
            checkmark_x = text_x + note_text.get_width() + 10
            checkmark_y = text_y
            screen.blit(checkmark, (checkmark_x, checkmark_y))


# Função para lidar com a primeira fase do jogo


def start_ilha_notas():
    global running, notes_found
    pygame.mixer.music.fadeout(1000)
    fade_in_ilha_notas()
    running = True
    dialogue_index = 0
    dialogue_finished = False
    note_positions = []
    dialogue_texts = [
        "Olá, bem-vindo à Ilha das Notas! Aqui, vamos explorar as sete notas musicais básicas.",
        "As notas são: Dó, Ré, Mi, Fá, Sol, Lá, Si.",
        "Cada uma tem seu som único e vibração.",
        "Vamos começar com Dó, a base para começar escalas e lições na música ocidental.",
        "Siga-me e tente identificar cada nota que encontrarmos pela ilha!",
        "Pressione Enter para continuar ou ESC para voltar ao menu."
    ]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if dialogue_index < len(dialogue_texts) - 1:
                        dialogue_index += 1
                    else:
                        dialogue_finished = True
                        note_positions = [(random.randint(
                            100, WIDTH - 200), random.randint(100, HEIGHT - 200)) for _ in range(len(note_sprites))]
                elif event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and dialogue_finished:
                mouse_x, mouse_y = event.pos
                check_note_click(mouse_x, mouse_y, notes_found, note_positions)
        screen.blit(primeiro_mundo_background, (0, 0))
        if dialogue_finished:
            draw_notes_and_confirmation(notes_found, note_positions)
            draw_note_legend()
        else:
            draw_guide_and_dialogue(dialogue_texts[dialogue_index])
        pygame.display.update()


def draw_notes_and_confirmation(notes_found, positions):
    for i, (note_name, sprite) in enumerate(note_sprites.items()):
        x, y = positions[i]  # Certifique-se de que esta posição está definida
        screen.blit(sprite, (x, y))
        if notes_found[i]:
            pygame.draw.circle(
                screen, (0, 255, 0), (x + sprite.get_width() // 2, y + sprite.get_height() // 2), 15)


def check_note_click(mouse_x, mouse_y, notes_found, positions):
    note_width, note_height = 100, 100  # Largura e altura dos sprites das notas
    for i, (x, y) in enumerate(positions):
        note_rect = pygame.Rect(x, y, note_width, note_height)
        if note_rect.collidepoint(mouse_x, mouse_y):
            notes_found[i] = True  # Certifique-se de que este índice existe
            break


def draw_guide_and_dialogue(text):
    # Posição do sprite do guia na tela
    guide_x = 100
    guide_y = HEIGHT // 2 - guide_sprite.get_height() // 2
    screen.blit(guide_sprite, (guide_x, guide_y))

    # Configurações para a caixa de diálogo
    dialog_width = WIDTH - 200
    dialog_height = 100
    dialog_x = 50
    dialog_y = HEIGHT - dialog_height - 50
    padding = 10  # Padding para o texto dentro da caixa

    # Desenha o retângulo para a caixa de diálogo
    pygame.draw.rect(screen, (0, 0, 0, 180), (dialog_x,
                     dialog_y, dialog_width, dialog_height))

    # Configura a fonte e renderiza o texto
    font = pygame.font.Font('resources/fonts/barcadenobar.ttf', 20)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (dialog_x + padding, dialog_y + padding)
    screen.blit(text_surface, text_rect)

    # Adiciona "Clique para continuar" no canto direito
    continue_text = font.render("clique para continuar", True, WHITE)
    continue_rect = continue_text.get_rect()
    continue_rect.bottomright = (
        dialog_x + dialog_width - padding - 10, dialog_y + dialog_height - padding)
    screen.blit(continue_text, continue_rect)

    # Adiciona uma setinha piscante
    current_time = pygame.time.get_ticks()
    if (current_time // 500) % 2:  # Piscar a cada 500 ms
        arrow_text = font.render(">", True, WHITE)
        arrow_rect = arrow_text.get_rect()
        arrow_rect.left = continue_rect.right + 5
        arrow_rect.centery = continue_rect.centery
        screen.blit(arrow_text, arrow_rect)

    # Desenha as bordas da caixa de diálogo
    pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y,
                     dialog_width, dialog_height), 2)
# Função para suavizar a transição para a fase


def fade_out_screen():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

# Função para suavizar a transição de volta ao menu


def fade_in_screen():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(300, 0, -1):
        fade.set_alpha(alpha)
        screen.blit(menu_background, (0, 0))
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)


def fade_in_ilha_notas():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(300, 0, -1):
        fade.set_alpha(alpha)
        screen.blit(primeiro_mundo_background, (0, 0))
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

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
                if selected_option == 0:  # Novo Jogo
                    start_ilha_notas()
                elif selected_option == len(menu_options) - 1:
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
