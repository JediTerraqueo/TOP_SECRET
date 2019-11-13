import pygame
from pygame.locals import *
import sys
import os

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

W, H = 1600,900
HW, HH = W / 2, H / 2
AREA = W * H

pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("TESTANDO O PARALLAX")
FPS = 120

bkgd = pygame.image.load("Fundo em 8 bits_3.png").convert()
x = 0

while True:
    events()

    rel_x = x % bkgd.get_rect().width
    DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
    if rel_x < W:
        DS.blit(bkgd,(rel_x, 0))
    x -= 1
    pygame.display.update()
    CLOCK.tick(FPS)


