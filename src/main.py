import pygame

pygame.init()

x = 1280
y = 720

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Music Game')

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
