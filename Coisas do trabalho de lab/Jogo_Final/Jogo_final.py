import os
import sys
from random import randrange

import pygame
from pygame.locals import *

import pygameMenu
from PPlay import (animation, collision, gameimage, gameobject, keyboard,
                   sprite, window)

sys.path.insert(0, '../../')

# -------------------------------------------------------------------------
# Variaveis uteis
# -------------------------------------------------------------------------
pygame.init()
velocidade = 8
W = 800
H = 600
BLACK = (0, 0, 0)
lives = 3
COLOR_BACKGROUND = (0, 0, 0)
COLOR_BLACK = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)
DIFFICULTY = ['EASY']
FPS = 60.0
MENU_BACKGROUND_COLOR = (0, 0, 0)
WINDOW_SIZE = (W , H)
walkCount = 0
luz_count = 10
X = 0
music = pygame.mixer.music.load('sounds/Fundo começo do mapa.mp3')
pygame.mixer.music.play(-1)

clock = None
main_menu = None
surface = None

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

def change_difficulty(value, difficulty):

    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
    DIFFICULTY[0] = difficulty


def random_color():

    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty, font, test=False):

    assert isinstance(difficulty, (tuple, list))
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    # Define globals
    global main_menu
    global clock

    # -------------------------------------------------------------------------
    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    # -------------------------------------------------------------------------
    main_menu.disable()
    main_menu.reset(1)

    while True:

        # -------------------------------------------------------------------------
        # Clock tick
        # -------------------------------------------------------------------------
        clock.tick(60)


        # -------------------------------------------------------------------------
        # Application events
        # -------------------------------------------------------------------------
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    # -------------------------------------------------------------------------
                    # Quit this function, then skip to loop of main-menu on line 317
                    # -------------------------------------------------------------------------
                    return

        # -------------------------------------------------------------------------
        # Pass events to main_menu
        # -------------------------------------------------------------------------
        main_menu.mainloop(events)

        win = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Tapa Buraco")
        walkRight = [pygame.image.load('spritesH/R1.png'), pygame.image.load('spritesH/R2.png'), pygame.image.load('spritesH/R3.png'),
                     pygame.image.load('spritesH/R4.png'), pygame.image.load('spritesH/R5.png'), pygame.image.load('spritesH/R6.png'),
                     pygame.image.load('spritesH/R7.png'), pygame.image.load('spritesH/R8.png'), pygame.image.load('spritesH/R9.png')]
        walkLeft = [pygame.image.load('spritesH/L1.png'), pygame.image.load('spritesH/L2.png'), pygame.image.load('spritesH/L3.png'),
                    pygame.image.load('spritesH/L4.png'), pygame.image.load('spritesH/L5.png'), pygame.image.load('spritesH/L6.png'),
                    pygame.image.load('spritesH/L7.png'), pygame.image.load('spritesH/L8.png'), pygame.image.load('spritesH/L9.png')]
        atk_left = [pygame.image.load('itens/machado_1.1_left.png'), pygame.image.load('itens/machado_1.2_left.png'),
                    pygame.image.load('itens/machado_1.3_left.png'), pygame.image.load('itens/machado_1.4_left.png')]
        atk_right = [pygame.image.load('itens/machado_2.1_right.png'), pygame.image.load('itens/machado_2.2_right.png'),
                     pygame.image.load('itens/machado_2.3_right.png'), pygame.image.load('itens/machado_2.4_right.png')]

        hitsound = pygame.mixer.Sound('sounds/hit.wav')
        man_hitsound = pygame.mixer.Sound('sounds/efeito de quando toma um dano.wav')
        man_hitsound_2 = pygame.mixer.Sound('sounds/efeito de quando toma um dano_2.wav')
        healsound = pygame.mixer.Sound('sounds/craocraocrao.wav')
        clock = pygame.time.Clock()
        score = 0
        count_fundo = 3

        # -------------------------------------------------------------------------
        # Classe do jogador
        # -------------------------------------------------------------------------
        class player(object):

            def __init__(self, x, y, W, H):
                self.x = x
                self.y = y
                self.W = W
                self.H = H
                self.vel = 5
                self.isJump = False
                self.left = False
                self.right = False
                self.standing = True
                self.walkCount = 0
                self.jumpCount = 10
                self.hitbox = (self.x + 17, self.y + 11 , 29, 52)
                self.health = 250
                self.stamina = 100
                self.mana = 60
                self.timer = 0
                self.damage = 50
                self.manacoust = 10
                self.staminacoust = 20

            # -------------------------------------------------------------------------
            # Desenha o player
            # -------------------------------------------------------------------------
            def draw(self,win):
                if self.walkCount + 1 >= 27:
                    self.walkCount = 0
                if not self.standing:
                    if self.left:
                        win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                    elif self.right:
                        win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                else:
                    if self.right:
                        win.blit(walkRight[0], (self.x, self.y))
                    else:
                        win.blit(walkLeft[0], (self.x, self.y))

                pygame.draw.rect(win, (168,168,168), (10, 20, 250, 15))
                pygame.draw.rect(win, (255,0,0), (10, 20, 50 - (50 - self.health), 15))
                pygame.draw.rect(win, (168,168,168), (10, 40, 100, 15))
                pygame.draw.rect(win, (0,255,0), (10, 40, 100 - (100 - self.stamina), 15))
                pygame.draw.rect(win, (168,168,168), (10, 60, 50, 15))
                pygame.draw.rect(win, (0,0,255), (10, 60, 100 - (110 - self.mana), 15))
                self.hitbox = (self.x + 17, self.y + 11 , 29, 52)

            # -------------------------------------------------------------------------
            # Função que mostra quando algo acerta o player
            # -------------------------------------------------------------------------
            def hit(self):

                if self.health > 0:
                    self.health -= self.damage
                    print(self.health)

                    if self.health <= 0:
                        k = 0
                        while k < 100:
                            font2 = pygame.font.SysFont('comicsans', 100, True)
                            ENDGAME = font2.render('G A M E  O V E R', 1, (255,255,255))
                            win.blit(ENDGAME, (70, 290))
                            pygame.display.update()
                            pygame.time.delay(10)
                            k += 1
                        if __name__ == '__main__':
                            main()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                    if self.right:
                        self.x = self.x - 50
                    elif self.left:
                        self.x = self.x + 50
                    elif self.isJump:
                        pass
                    self.walkCount = 0
                    font1 = pygame.font.SysFont('comicsans', 32, True)
                    text = font1.render('-5', 1, (255,255,255))
                    win.blit(text, (725, 50))
                    pygame.display.update()
                    i = 0

                    while i < 11:
                        pygame.time.delay(10)
                        i += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                i = 11
                                pygame.quit()

        # -------------------------------------------------------------------------
        # Classe do inimigo
        # -------------------------------------------------------------------------
        class enemy(object):
            walkRight = [pygame.image.load('spritesE/R1E.png'), pygame.image.load('spritesE/R2E.png'), pygame.image.load('spritesE/R3E.png'),
                         pygame.image.load('spritesE/R4E.png'), pygame.image.load('spritesE/R5E.png'), pygame.image.load('spritesE/R6E.png'),
                         pygame.image.load('spritesE/R7E.png'), pygame.image.load('spritesE/R8E.png'), pygame.image.load('spritesE/R9E.png'),
                         pygame.image.load('spritesE/R10E.png'), pygame.image.load('spritesE/R11E.png')]
            walkLeft = [pygame.image.load('spritesE/L1E.png'), pygame.image.load('spritesE/L2E.png'), pygame.image.load('spritesE/L3E.png'),
                        pygame.image.load('spritesE/L4E.png'), pygame.image.load('spritesE/L5E.png'), pygame.image.load('spritesE/L6E.png'),
                        pygame.image.load('spritesE/L7E.png'), pygame.image.load('spritesE/L8E.png'), pygame.image.load('spritesE/L9E.png'),
                        pygame.image.load('spritesE/L10E.png'), pygame.image.load('spritesE/L11E.png')]
            colision = [pygame.image.load('spritesE/explosão_1.png'), pygame.image.load('spritesE/explosão_2.png'), pygame.image.load('spritesE/explosão_3.png'),
                        pygame.image.load('spritesE/explosão_4.png'), pygame.image.load('spritesE/explosão_5.png'), pygame.image.load('spritesE/explosão_6.png')]
            #resurection = [pygame.image.load('fase-1.png'), pygame.image.load('fase-2.png'), pygame.image.load('fase-3.png'),
            #              pygame.image.load('fase-4.png'), pygame.image.load('fase-5.png'), pygame.image.load('fase-6.png'),
            #             pygame.image.load('fase-7.png'), pygame.image.load('fase-8.png'), pygame.image.load('fase-9.png'),
            #            pygame.image.load('fase-10.png'), pygame.image.load('fase-11.png'), pygame.image.load('fase-12.png'),
            #           pygame.image.load('fase-13.png'), pygame.image.load('fase-14.png'), pygame.image.load('fase-15.png'),
            #          pygame.image.load('fase-16.png'), pygame.image.load('fase-17.png'), pygame.image.load('fase-18.png')]

            def __init__(self, x ,y, W, H, end):
                self.x = x
                self.y = y
                self.W = W
                self.H = H
                self.end = end
                self.path = [self.x, 700]
                self.walkCount = 0
                self.vel = 3
                self.time = 0
                self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                self.health = 10
                self.visible = True
                self.isjump = False
                self.left = False
                self.right = False
                self.jumpcount = 10
                self.Count = 0
                self.escolha = True

            # -------------------------------------------------------------------------
            # Função que desenha o personagem
            # -------------------------------------------------------------------------
            def draw(self,win):
                self.move()
                if self.visible:
                    self.time = 0
                    if self.walkCount + 1 >= 33:
                        self.walkCount = 0
                    if self.vel > 0:
                        win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1

                    if self.vel < 0:
                        win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1

                    pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                    pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5*(10 - self.health)), 10))
                    self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                else:
                    self.escolha = False
                    if not self.time + 1 >= 13:
                        win.blit(self.colision[self.time // 2], (self.x, self.y - 55))
                        self.time += 1

            # -------------------------------------------------------------------------
            # Função para movimentar o inimigo
            # -------------------------------------------------------------------------
            def move(self):
                if self.escolha:
                    if not goblin.isjump:
                        self.Count += 1
                        if self.Count == 75:
                            goblin.isjump = True
                            goblin.left = False
                            goblin.right = False
                            goblin.walkCount = 0
                            self.Count = 0
                    else:
                        if goblin.jumpcount >= -10:
                            goblin.y -= (goblin.jumpcount * abs(goblin.jumpcount)) * 0.5
                            goblin.jumpcount -= 1
                        else:
                            goblin.jumpcount = 10
                            goblin.isjump = False
                    if self.vel > 0:
                        if self.x  + self.vel < self.path[1]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0
                    else:
                        if self.x - self.vel > self.path[0]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0

            # -------------------------------------------------------------------------
            # Função para quando o inimigo receber um ataque
            # -------------------------------------------------------------------------
            def hit_pitchfork(self):
                if self.health > 0:
                    self.health -= 20
                    if self.health < 0:
                        goblin.visible = False
                else:
                    self.visible = False
                print("hit")

            def hit_axe(self):
                if self.health > 0:
                    self.health -= 1
                else:
                    self.visible = False
                print("hit")


        class enemy2(object):
            walkRight = [pygame.image.load('spritesE/R1E.png'), pygame.image.load('spritesE/R2E.png'), pygame.image.load('spritesE/R3E.png'),
                         pygame.image.load('spritesE/R4E.png'), pygame.image.load('spritesE/R5E.png'), pygame.image.load('spritesE/R6E.png'),
                         pygame.image.load('spritesE/R7E.png'), pygame.image.load('spritesE/R8E.png'), pygame.image.load('spritesE/R9E.png'),
                         pygame.image.load('spritesE/R10E.png'), pygame.image.load('spritesE/R11E.png')]
            walkLeft = [pygame.image.load('spritesE/L1E.png'), pygame.image.load('spritesE/L2E.png'), pygame.image.load('spritesE/L3E.png'),
                        pygame.image.load('spritesE/L4E.png'), pygame.image.load('spritesE/L5E.png'), pygame.image.load('spritesE/L6E.png'),
                        pygame.image.load('spritesE/L7E.png'), pygame.image.load('spritesE/L8E.png'), pygame.image.load('spritesE/L9E.png'),
                        pygame.image.load('spritesE/L10E.png'), pygame.image.load('spritesE/L11E.png')]
            colision = [pygame.image.load('spritesE/explosão_1.png'), pygame.image.load('spritesE/explosão_2.png'), pygame.image.load('spritesE/explosão_3.png'),
                        pygame.image.load('spritesE/explosão_4.png'), pygame.image.load('spritesE/explosão_5.png'), pygame.image.load('spritesE/explosão_6.png')]
            #resurection = [pygame.image.load('fase-1.png'), pygame.image.load('fase-2.png'), pygame.image.load('fase-3.png'),
            #              pygame.image.load('fase-4.png'), pygame.image.load('fase-5.png'), pygame.image.load('fase-6.png'),
            #             pygame.image.load('fase-7.png'), pygame.image.load('fase-8.png'), pygame.image.load('fase-9.png'),
            #            pygame.image.load('fase-10.png'), pygame.image.load('fase-11.png'), pygame.image.load('fase-12.png'),
            #           pygame.image.load('fase-13.png'), pygame.image.load('fase-14.png'), pygame.image.load('fase-15.png'),
            #          pygame.image.load('fase-16.png'), pygame.image.load('fase-17.png'), pygame.image.load('fase-18.png')]

            def __init__(self, x ,y, W, H, end):
                self.x = x
                self.y = y
                self.W = W
                self.H = H
                self.end = end
                self.path = [self.x, 700]
                self.walkCount = 0
                self.vel = 3
                self.time = 0
                self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                self.health = 10
                self.visible = True
                self.isjump = False
                self.left = False
                self.right = False
                self.jumpcount = 10
                self.Count = 0
                self.escolha = True

            # -------------------------------------------------------------------------
            # Função que desenha o personagem
            # -------------------------------------------------------------------------
            def draw(self,win):
                self.move()
                if self.visible:
                    self.time = 0
                    if self.walkCount + 1 >= 33:
                        self.walkCount = 0
                    if self.vel > 0:
                        win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1

                    if self.vel < 0:
                        win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1

                    pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                    pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5*(10 - self.health)), 10))
                    self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                else:
                    self.escolha = False
                    if not self.time + 1 >= 13:
                        win.blit(self.colision[self.time // 2], (self.x, self.y - 55))
                        self.time += 1

            # -------------------------------------------------------------------------
            # Função para movimentar o inimigo
            # -------------------------------------------------------------------------
            def move(self):
                if self.escolha:
                    if not self.isjump:
                        self.Count += 1
                        if self.Count == 75:
                            self.isjump = True
                            self.left = False
                            self.right = False
                            self.walkCount = 0
                            self.Count = 0
                    else:
                        if self.jumpcount >= -10:
                            self.y -= (self.jumpcount * abs(self.jumpcount)) * 0.5
                            self.jumpcount -= 1
                        else:
                            self.jumpcount = 10
                            self.isjump = False
                    if self.vel > 0:
                        if self.x  + self.vel < self.path[1]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0
                    else:
                        if self.x - self.vel > self.path[0]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0

            # -------------------------------------------------------------------------
            # Função para quando o inimigo receber um ataque
            # -------------------------------------------------------------------------
            def hit_pitchfork(self):
                if self.health > 0:
                    self.health -= 20
                    if self.health < 0:
                        self.visible = False
                else:
                    self.visible = False
                print("hit")

            def hit_axe(self):
                if self.health > 0:
                    self.health -= 1
                else:
                    self.visible = False
                print("hit")



        # -------------------------------------------------------------------------
        # Classes do ataque, mana e cura
        # -------------------------------------------------------------------------
        class atk(object):

            def __init__(self, x, y, facing, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h
                self.facing = facing
                self.vel = 12 * facing
                self.hitbox = (self.x, self.y, w, h)
                self.spins = 0

            def draw(self,win):
                if man.health > 0:
                    if self.spins + 1 >= 17:
                        self.spins = 0

                    if self.vel > 0:
                        win.blit(atk_right[self.spins // 4], (self.x, self.y))
                        self.spins += 1

                    if self.vel < 0:
                        win.blit(atk_left[self.spins // 4], (self.x - 50, self.y))
                        self.spins += 1



        # -------------------------------------------------------------------------
        # Classe do projetil pitchfork
        # -------------------------------------------------------------------------
        class projectile(object):
            pitchfork_right = pygame.image.load('itens/pitchfork_right.png')
            pitchfork_left = pygame.image.load('itens/pitchfork_left.png')
            def __init__(self, x, y, facing, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h
                self.facing = facing
                self.vel = 12 * facing
                self.hitbox = (self.x, self.y, w, h)

            # -------------------------------------------------------------------------
            # Função que desenha o pitchfork na tela
            # -------------------------------------------------------------------------
            def draw(self,win):
                if self.vel > 0:
                    win.blit(self.pitchfork_right, (self.x, self.y))

                elif self.vel < 0:
                    win.blit(self.pitchfork_left, (self.x - 120, self.y))

        # -------------------------------------------------------------------------
        # Classe da mana
        # -------------------------------------------------------------------------
        class Mana(object):
            Mana = pygame.image.load('consumivel/mana_flask.png')
            def __init__(self, x ,y, w, h, rel_x):
                self.mana_visible = True
                self.mana_x = x
                self.mana_y = y
                self.width = w
                self.height = h
                self.rel_x = rel_x
                self.hitbox = (self.mana_x, self.mana_y, w, h)

            # -------------------------------------------------------------------------
            # Função que desenha a mana na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                if self.mana_visible:
                    win.blit(self.Mana, (self.mana_x, self.mana_y))

            # -------------------------------------------------------------------------
            # Função que reenche a mana
            # -------------------------------------------------------------------------
            def replenish_mana(self):
                man.mana += 10
                self.mana_visible = False
                pygame.display.update()

        # -------------------------------------------------------------------------
        # Classe da cura
        # -------------------------------------------------------------------------
        class Cure(object):
            heart = pygame.image.load('consumivel/health_flask.png')
            def __init__(self, x, y, w, h, rel_x):
                self.heal_visible = True
                self.heal_x = x
                self.heal_y = y
                self.width = w
                self.height = h
                self.rel_x = rel_x
                self.hitbox = (self.heal_x, self.heal_y, w, h)

            # -------------------------------------------------------------------------
            # Função que desenha a cura na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                if heal.heal_visible:
                    win.blit(self.heart, (self.heal_x, self.heal_y))
            # -------------------------------------------------------------------------
            # Função que reenche a vida
            # -------------------------------------------------------------------------
            def cure(self):
                man.health += 50
                heal.heal_visible = False
                pygame.display.update()

        # -------------------------------------------------------------------------
        # Classes do parallax
        # -------------------------------------------------------------------------
        class parallax(object):
            parallax = pygame.image.load('fundo/fundo parallax.png')
            def __init__(self, x, y, w, h, rel_x):
                self.x = x
                self.y = y
                self.width = w
                self.height = h
                self.rel_x = rel_x

            # -------------------------------------------------------------------------
            # Desenha o parallax na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                self.rel_x = self.x % fundo.bg.get_rect().width
                win.blit(self.parallax, (self.rel_x - self.parallax.get_rect().width, 0))
                if self.rel_x < W:
                    win.blit(self.parallax, (self.rel_x, 0))
                self.x -= 2.5

        # -------------------------------------------------------------------------
        # Classe do fundo
        # -------------------------------------------------------------------------
        class fundo(object):
            bg = pygame.image.load('fundo/fundo_1.png')
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h

            # -------------------------------------------------------------------------
            # Funçao que desenha o fundo
            # -------------------------------------------------------------------------
            def draw(self, win):
                win.blit(self.bg, (0, 0))

        class fundo_2(object):
            bg_2 = pygame.image.load('fundo/fundo_2.png')
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h

            def draw(self, win):
                win.blit(self.bg_2, (0, 0))

        class fundo_3(object):
            bg_3 = pygame.image.load('fundo/fundo_3.png')
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h

            def draw(self, win):
                win.blit(self.bg_3, (0, 0))

        class fundo_4(object):
            bg_4 = pygame.image.load('fundo/fundo_4.png')
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h

            def draw(self, win):
                win.blit(self.bg_4, (0, 0))
        # -------------------------------------------------------------------------
        # Classe do consumivel de cura
        # -------------------------------------------------------------------------
        class consumivel_health(object):
            consumivel_1 = pygame.image.load('itens/consumivel_1.png')
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.counter = 0

            # -------------------------------------------------------------------------
            # Função que desenha o consumivel de cura na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                win.blit(self.consumivel_1, (self.x, self.y))

            # -------------------------------------------------------------------------
            # Função que reenche a vida a partir do consumivel
            # -------------------------------------------------------------------------
            def heal(self):
                man.health += 50
                self.counter -= 1

        # -------------------------------------------------------------------------
        # Classe do consumivel de mana
        # -------------------------------------------------------------------------
        class consumivel_mana(object):
            consumivel_2 = pygame.image.load('itens/consumivel_2.png')
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.counter = 0

            # -------------------------------------------------------------------------
            # Função que desenha o consumivel de mana na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                win.blit(self.consumivel_2, (self.x, self.y))

            # -------------------------------------------------------------------------
            # Função que reenche a mana a partir do consumivel de mana
            # -------------------------------------------------------------------------
            def replenish(self):
                man.mana += 10
                self.counter -= 1

        # -------------------------------------------------------------------------
        # classe do hud
        # -------------------------------------------------------------------------
        class hud(object):
            hud = pygame.image.load('images/Hud basico.png')
            def __init__(self, x, y):
                self.x = x
                self.y = y

            # -------------------------------------------------------------------------
            # Função que desenha o hud na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                win.blit(self.hud, (self.x, self.y))

        # -------------------------------------------------------------------------
        # Classe da plataforma
        # -------------------------------------------------------------------------
        class plataforma(object):
            plataformer = pygame.image.load('images/plataforma.png')
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hitbox = (self.x, self.y, w, h)

            # -------------------------------------------------------------------------
            # Função que desenha a plataforma na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                win.blit(self.plataformer, (self.x, self.y))

        class plataforma_2(object):
            plataformer = pygame.image.load('images/plataforma.png')
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hitbox = (self.x, self.y, w, h)

            # -------------------------------------------------------------------------
            # Função que desenha a plataforma na tela
            # -------------------------------------------------------------------------
            def draw(self, win):
                win.blit(self.plataformer, (self.x, self.y))

        class camera_decente(object):
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hitbox = (self.x, self.y, w, h)

        class aneis(object):
            _0_anel = pygame.image.load("itens_E/0 aneis.png")
            _1_v_anel = pygame.image.load("itens_E/vermelho.png")
            _1_ve_anel = pygame.image.load("itens_E/verde.png")
            _1_a_anel = pygame.image.load("itens_E/azul.png")
            _2_anel_v_ve = pygame.image.load("itens_E/2 aneis_v_ve.png")
            _2_anel_v_a = pygame.image.load("itens_E/2 aneis_v_a.png")
            _2_anel_ve_a = pygame.image.load("itens_E/2 aneis_a_ve.png")
            _3_anel = pygame.image.load("itens_E/3 aneis.png")

            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.a_1 = False
                self.a_2 = False
                self.a_3 = False

            #a_1 vermelho
            #a_2 verde
            #a_3 azul

            def draw(self, win):
#------------------------------------------------------------------------------
                if not self.a_1 and not self.a_2 and not self.a_3:
                    win.blit(self._0_anel, (self.x, self.y))
#------------------------------------------------------------------------------
                elif self.a_1 and not self.a_2 and not self.a_3:
                    win.blit(self._1_v_anel, (self.x, self.y))
                elif not self.a_1 and self.a_2 and not self.a_3:
                    win.blit(self._1_ve_anel, (self.x, self.y))
                elif not self.a_1 and not self.a_2 and self.a_3:
                    win.blit(self._1_a_anel, (self.x, self.y))
#------------------------------------------------------------------------------
                elif self.a_1 and self.a_2 and not self.a_3:
                    win.blit(self._2_anel_v_ve, (self.x, self.y))
                elif not self.a_1 and self.a_2 and self.a_3:
                    win.blit(self._2_anel_ve_a, (self.x, self.y))
                elif self.a_1 and not self.a_2 and self.a_3:
                    win.blit(self._2_anel_v_a, (self.x, self.y))
#------------------------------------------------------------------------------
                elif self.a_1 and self.a_2 and self.a_3:
                    win.blit(self._3_anel, (self.x, self.y))
#------------------------------------------------------------------------------

        class anel_1(object):
            anel_v = pygame.image.load("itens_E/vermelho solo.png")
            anel_v_t = pygame.image.load("itens_E/vermelho pego.png")
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hitbox = (self.x, self.y, w, h)
                self.visible = True

            def draw(self, win):
                if anel_1.visible:
                    win.blit(self.anel_v, (self.x, self.y))

            def draw_taking(self, win):
                win.blit(self.anel_v_t, (man.x, man.y))

        class anel_2(object):
            anel_ve = pygame.image.load("itens_E/verde solo.png")
            anel_ve_t = pygame.image.load("itens_E/verde pego.png")
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hitbox = (self.x, self.y, w, h)
                self.visible = True

            def draw(self, win):
                if anel_2.visible:
                    win.blit(self.anel_ve, (self.x, self.y))

            def draw_taking(self, win):
                win.blit(self.anel_ve_t, (man.x, man.y))

        class anel_3(object):
            anel_a = pygame.image.load("itens_E/azul solo.png")
            def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hitbox = (self.x, self.y, w, h)
                self.visible = True

            def draw(self, win):
                if anel_3.visible:
                    win.blit(self.anel_a, (self.x, self.y))

        class bloodboss(object):
            walkRight = [pygame.image.load('spritesE/bosses/pose1r.png'), pygame.image.load('spritesE/bosses/pose2r.png'), pygame.image.load('spritesE/bosses/pose3r.png'),
                         pygame.image.load('spritesE/bosses/pose4r.png'), pygame.image.load('spritesE/bosses/pose5r.png'), pygame.image.load('spritesE/bosses/pose6r.png')]
            walkLeft = [pygame.image.load('spritesE/bosses/pose1l.png'), pygame.image.load('spritesE/bosses/pose2l.png'), pygame.image.load('spritesE/bosses/pose3l.png'),
                        pygame.image.load('spritesE/bosses/pose4l.png'), pygame.image.load('spritesE/bosses/pose5l.png'), pygame.image.load('spritesE/bosses/pose6l.png')]
            colision = [pygame.image.load('spritesE/explosão_1.png'), pygame.image.load('spritesE/explosão_2.png'), pygame.image.load('spritesE/explosão_3.png'),
                        pygame.image.load('spritesE/explosão_4.png'), pygame.image.load('spritesE/explosão_5.png'), pygame.image.load('spritesE/explosão_6.png')]
            hud = pygame.image.load('spritesE/bosses/hud bloodboss.png')

            def __init__(self, x, y, w, h, end):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.end = end
                self.path = [self.x, 700]
                self.walkCount = 0
                self.vel = 5
                self.time = 0
                self.hitbox = (self.x , self.y, 119, 115)
                self.health = 200
                self.visible = True
                self.isjump = False
                self.left = False
                self.right = False
                self.jumpcount = 10
                self.Count = 0
                self.escolha = True
                self.atk = False
                self.countatk = 0

            def draw(self,win):
                self.move()
                if self.visible:
                    self.time = 0
                    if self.walkCount + 1 >= 24:
                        self.walkCount = 0
                    if self.vel > 0:
                        win.blit(self.walkRight[self.walkCount // 4], (self.x, self.y))
                        self.walkCount += 1

                    if self.vel < 0:
                        win.blit(self.walkLeft[self.walkCount // 4], (self.x, self.y))
                        self.walkCount += 1

                    win.blit(self.hud, (200, 89))
                    pygame.draw.rect(win, (255,0,0), (201, 100, 395, 10))
                    pygame.draw.rect(win, (0,255,0), (201, 100, 51 - (2*(28 - self.health)), 10))
                    pygame.draw.rect(win, (255,0,0), self.hitbox,2)
                    self.hitbox = (self.x , self.y, 119, 115 + 40)
                else:
                    self.escolha = False
                    if not self.time + 1 >= 13:
                        win.blit(self.colision[self.time // 2], (self.x, self.y - 55))
                        self.time += 1

            # -------------------------------------------------------------------------
            # Função para movimentar o inimigo
            # -------------------------------------------------------------------------
            def move(self):
                if self.escolha:
                    if not self.isjump:
                        self.Count += 1
                        if self.Count == 75:
                            self.isjump = True
                            self.left = False
                            self.right = False
                            self.walkCount = 0
                            self.Count = 0
                    else:
                        if self.jumpcount >= -10:
                            self.y -= (self.jumpcount * abs(self.jumpcount)) * 0.5
                            self.jumpcount -= 1
                        else:
                            self.jumpcount = 10
                            self.isjump = False
                    if self.vel > 0:
                        if self.x  + self.vel < self.path[1]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0
                    else:
                        if self.x - self.vel > self.path[0]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0

        # -------------------------------------------------------------------------
            # Função para quando o inimigo receber um ataque
            # -------------------------------------------------------------------------
            def hit_pitchfork(self):

                if self.health > 0:
                    if anel_count == 3:
                        self.health -= 100
                    self.health -= 20
                    if self.health < 0:
                        k = 0
                        bloodboss.visible = False
                        while k < 100:
                            font2 = pygame.font.SysFont('comicsans', 80, True)
                            CONGRATS = font2.render('YOU WIN CONGRATS', 1, (255,255,255))
                            win.blit(CONGRATS, (70, 290))
                            pygame.display.update()
                            pygame.time.delay(10)
                            k += 1
                        if __name__ == '__main__':
                            main()
                else:
                    self.visible = False
                print("hit")

            def hit_axe(self):
                if self.health > 0:
                    self.health -= 10
                else:
                    k = 0
                    self.visible = False
                    while k < 100:
                        font2 = pygame.font.SysFont('comicsans', 80, True)
                        CONGRATS = font2.render('YOU WIN CONGRATS', 1, (255,255,255))
                        win.blit(CONGRATS, (70, 290))
                        pygame.display.update()
                        pygame.time.delay(10)
                        k += 1
                    if __name__ == '__main__':
                        main()
                print("hit")

        # -------------------------------------------------------------------------
        # Função que desenha as imagens na tela
        # -------------------------------------------------------------------------
        def redrawgamewindow():
            parallax.draw(win)
            if count_fundo == 0:
                fundo.draw(win)
                plataforma.draw(win)
                plataforma_2.draw(win)
                plataforma_2.x, plataforma_2.y = 150, 270
                plataforma_2.hitbox = (150, 250, plataforma.w, plataforma.h)
                goblin.x = goblin.x
                goblin.y = goblin.y
                goblin2.x = goblin2.x
                goblin2.y = goblin2.y
                plataforma.x, plataforma.y = 400, 400
                plataforma.hitbox = (400, 400, plataforma.w, plataforma.h)
                goblin.draw(win)
                goblin2.draw(win)
                anel_1.draw(win)
                heal.draw(win)
                mana.draw(win)

            elif count_fundo == 1:
                fundo_2.draw(win)
                plataforma.draw(win)
                goblin.x = goblin.x
                goblin.y = goblin.y
                goblin2.x = goblin2.x
                goblin2.y = goblin2.y
                plataforma.x, plataforma.y = 600, 300
                plataforma.hitbox = (600, 300, plataforma.w, plataforma.h)
                goblin.draw(win)
                goblin2.draw(win)
                anel_2.draw(win)

            elif count_fundo == 2:
                fundo_3.draw(win)
                plataforma.draw(win)
                plataforma_2.draw(win)
                goblin.x = goblin.x
                goblin.y = goblin.y
                goblin2.x = goblin2.x
                goblin2.y = goblin2.y
                goblin.draw(win)
                goblin2.draw(win)
                plataforma.x, plataforma.y = 600, 300
                plataforma.hitbox = (600, 300, plataforma.w, plataforma.h)
                anel_3.draw(win)

            elif count_fundo == 3:
                fundo_4.draw(win)
                plataforma.draw(win)
                plataforma_2.draw(win)
                plataforma.x, plataforma.y = 600, 300
                plataforma_2.x, plataforma_2.y = 40, 300
                plataforma.hitbox = (plataforma.x, plataforma.y, plataforma.w, plataforma.h)
                plataforma_2.hitbox = (plataforma_2.x, plataforma_2.y, plataforma_2.w, plataforma_2.h)
                bloodboss.draw(win)

            text = font.render('Score: '+ str(score), 1, (255,255,255))
            text_1 = font_1.render(str(consumivel_h.counter), 1, (255,255,255))
            text_2 = font_1.render(str(consumivel_m.counter), 1, (255,255,255))
            text_c = font_2.render('C', 1, (255,255,255))
            text_v = font_2.render('V', 1, (255,255,255))
            aneis.draw(win)

            man.draw(win)
            hud.draw(win)
            consumivel_h.draw(win)
            consumivel_m.draw(win)
            win.blit(text_1, (320, 5))
            win.blit(text_2, (400, 5))
            win.blit(text_c, (362, 45))
            win.blit(text_v, (442, 45))
            win.blit(text, (650,25))
            for axe in axes:
                axe.draw(win)
            for bullet in bullets:
                bullet.draw(win)

            pygame.display.update()

        # -------------------------------------------------------------------------
        # variaveis uteis
        # -------------------------------------------------------------------------
        font = pygame.font.SysFont('Vampire Warz', 30, True)
        font_1 = pygame.font.SysFont('Vampire Warz', 30, True)
        font_2 = pygame.font.SysFont('Vampire Warz', 25, True)
        anel_1 = anel_1(150, 220, 26, 42)
        anel_2 = anel_2(600, 240, 26, 42)
        anel_3 = anel_3(150, 220, 26, 42)
        aneis = aneis(480, 5)
        man = player(10, 485, 64, 64)
        goblin = enemy(100, 490, 64, 64, 450)
        goblin2 = enemy2(50, 490, 64, 64, 450)
        bloodboss = bloodboss(100, 400, 119, 115, 450)
        heal = Cure(300, 500, 22, 55, 0)
        mana = Mana(200, 500, 22, 54, 0)
        parallax = parallax(0, 0, 1600, 600, 0)
        fundo = fundo(0, 0, 1600, 600)
        fundo_2 = fundo_2(0, 0, 1600, 600)
        fundo_3 = fundo_3(0, 0, 1600, 600)
        fundo_4 = fundo_4(0, 0, 1600, 600)
        plataforma = plataforma(400, 400, 170, 66)
        plataforma_2 = plataforma_2(400, 350, 170, 66)
        camera_decente = camera_decente(0, 0, 800, 600)

        hud = hud(-7, 2)
        consumivel_h = consumivel_health(320, 5)
        consumivel_m = consumivel_mana(400, 5)
        run = True
        bullets = []
        axes = []
        respawn = 0
        heal_respawn = 0
        mana_respawn = 0
        shootloop = 0
        anel_count = 0

        # -------------------------------------------------------------------------
        # main loop
        # -------------------------------------------------------------------------
        while run:
            while run:

                # -------------------------------------------------------------------------
                # Função que verifica se o heroi passou pelos cantos da tela
                # -------------------------------------------------------------------------
                if man.x > 800 and count_fundo < 3:
                    count_fundo += 1
                    man.x = -20
                if man.x < -20 and count_fundo >= 1 and count_fundo < 3:
                    count_fundo -= 1
                    man.x = 800

                if bloodboss.health < 0:
                    congrats.draw(win)

                # -------------------------------------------------------------------------
                # Função que verifica as hitboxes do goblin em relação a plataforma
                # -------------------------------------------------------------------------
                if goblin.visible:
                    if goblin.hitbox[1] < plataforma.hitbox[1] + plataforma.hitbox[3] and goblin.hitbox[1] + goblin.hitbox[3] > plataforma.hitbox[1] :
                        if goblin.hitbox[0] + goblin.hitbox[2] > plataforma.hitbox[0] and goblin.hitbox[0] < plataforma.hitbox[0] + plataforma.hitbox[2]:
                            goblin.y = plataforma.y - 55
                            if goblin.y < plataforma.y - 55:
                                goblin.y -= 25
                        else:
                            if not goblin.isjump:
                                goblin.y += 25
                    elif goblin.y < 480 and not goblin.isjump:
                        goblin.y += 25

                if goblin2.visible:
                    if goblin2.hitbox[1] < plataforma.hitbox[1] + plataforma.hitbox[3] and goblin2.hitbox[1] + goblin2.hitbox[3] > plataforma.hitbox[1] :
                        if goblin2.hitbox[0] + goblin2.hitbox[2] > plataforma.hitbox[0] and goblin2.hitbox[0] < plataforma.hitbox[0] + plataforma.hitbox[2]:
                            goblin2.y = plataforma.y - 55
                            if goblin2.y < plataforma.y - 55:
                                goblin2.y -= 25
                        else:
                            if not goblin2.isjump:
                                goblin2.y += 25
                    elif goblin2.y < 480 and not goblin2.isjump:
                        goblin2.y += 25
                # -------------------------------------------------------------------------
                # Função que verifica as hitboxes do man em relação a plataforma_2
                # -------------------------------------------------------------------------
                if man.hitbox[1] < plataforma_2.hitbox[1] + plataforma_2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > plataforma_2.hitbox[1]:
                    if man.hitbox[0] + man.hitbox[2] > plataforma_2.hitbox[0] and man.hitbox[0] < plataforma_2.hitbox[0] + plataforma_2.hitbox[2]:
                        man.y = plataforma_2.y  - 90
                    else:
                        if not man.isJump:
                            man.y += 25
                elif man.y < 465 and not man.isJump:
                    man.y += 25

                # -------------------------------------------------------------------------
                # Função que verifica as hitboxes do man em relação a plataforma
                # -------------------------------------------------------------------------
                if man.hitbox[1] < plataforma.hitbox[1] + plataforma.hitbox[3] and man.hitbox[1] + man.hitbox[3] > plataforma.hitbox[1]:
                    if man.hitbox[0] + man.hitbox[2] > plataforma.hitbox[0] and man.hitbox[0] < plataforma.hitbox[0] + plataforma.hitbox[2]:
                        man.y = plataforma.y - 60
                        if man.y < plataforma.y - 60:
                            man.y -= 30
                    else:
                        if not man.isJump:
                            man.y += 30
                elif man.y < 465 and not man.isJump:
                    man.y += 30

                # -------------------------------------------------------------------------
                # Função que da auto replenish na stamina
                # -------------------------------------------------------------------------
                if man.stamina < 100:
                    man.timer += 1
                    if man.timer >= 20:
                        man.stamina += 2
                elif man.stamina == 100:
                    man.timer = 0

                # -------------------------------------------------------------------------
                # Função que verifica se o goblin está vivo ou não
                # -------------------------------------------------------------------------
                if not goblin.visible:
                    respawn += 1
                    if respawn > 100:
                        respawn = 0
                        goblin.visible = True
                        goblin.escolha = True
                        goblin.health = 10

                if not goblin2.visible:
                    respawn += 1
                    if respawn > 100:
                        respawn = 0
                        goblin2.visible = True
                        goblin2.escolha = True
                        goblin2.health = 10

                # -------------------------------------------------------------------------
                # Função que verifica as hitboxes do goblin em relação ao man
                # -------------------------------------------------------------------------
                if goblin.visible:
                    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                            if man.health > 100:
                                man_hitsound.play()
                                man.hit()
                                score -= 5
                            elif man.health <= 100:
                                man_hitsound_2.play()
                                man.hit()
                                score -= 5

                if goblin2.visible:
                    if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                            if man.health > 100:
                                man_hitsound.play()
                                man.hit()
                                score -= 5
                            elif man.health <= 100:
                                man_hitsound_2.play()
                                man.hit()
                                score -= 5

                if bloodboss.visible and count_fundo == 3:
                    if man.hitbox[1] < bloodboss.hitbox[1] + bloodboss.hitbox[3] and man.hitbox[1] + man.hitbox[3] > bloodboss.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > bloodboss.hitbox[0] and man.hitbox[0] < bloodboss.hitbox[0] + bloodboss.hitbox[2]:
                            if man.health > 100:
                                man_hitsound.play()
                                man.hit()
                                score -= 15
                            elif man.health <= 100:
                                man_hitsound_2.play()
                                man.hit()
                                score -= 15

                # -------------------------------------------------------------------------
                # Função que faz o respawn do consumivel de cura
                # -------------------------------------------------------------------------
                if not heal.heal_visible:
                    heal_respawn += 1
                    if heal_respawn > 250:
                        heal_respawn = 0
                        heal.heal_visible = True

                #a_1 vermelho
                #a_2 verde
                #a_3 azul

                if not aneis.a_1 and count_fundo == 0:
                    if man.hitbox[1] < anel_1.hitbox[1] + anel_1.hitbox[3] and man.hitbox[1] + man.hitbox[3] > anel_1.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > anel_1.hitbox[0] and man.hitbox[0] < anel_1.hitbox[0] + anel_1.hitbox[2]:
                            aneis.a_1 = True
                            anel_1.visible = False
                            anel_count += 1
                            man.damage = 25

                if not aneis.a_2 and count_fundo == 1:
                    if man.hitbox[1] < anel_2.hitbox[1] + anel_2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > anel_2.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > anel_2.hitbox[0] and man.hitbox[0] < anel_2.hitbox[0] + anel_2.hitbox[2]:
                            aneis.a_2 = True
                            anel_2.visible = False
                            anel_count += 1
                            man.staminacoust = 10

                if not aneis.a_3 and count_fundo == 2:
                    if man.hitbox[1] < anel_3.hitbox[1] + anel_3.hitbox[3] and man.hitbox[1] + man.hitbox[3] > anel_3.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > anel_3.hitbox[0] and man.hitbox[0] < anel_3.hitbox[0] + anel_3.hitbox[2]:
                            aneis.a_3 = True
                            anel_3.visible = False
                            anel_count += 1
                            man.manacoust = 5

                # -------------------------------------------------------------------------
                # Função que verifica as hitboxes do man em relação a cura se visivel
                # -------------------------------------------------------------------------
                if heal.heal_visible and count_fundo == 0:
                    if man.health < 250:
                        if man.hitbox[1] < heal.hitbox[1] + heal.hitbox[3] and man.hitbox[1] + man.hitbox[3] > heal.hitbox[1]:
                            if man.hitbox[0] + man.hitbox[2] > heal.hitbox[0] and man.hitbox[0] < heal.hitbox[0] + heal.hitbox[2]:
                                healsound.play()
                                heal.cure()

                    # -------------------------------------------------------------------------
                    # Função para coletar e armazenar um coletavel de cura
                    # -------------------------------------------------------------------------
                    elif man.health >= 250:
                        if man.hitbox[1] < heal.hitbox[1] + heal.hitbox[3] and man.hitbox[1] + man.hitbox[3] > heal.hitbox[1]:
                            if man.hitbox[0] + man.hitbox[2] > heal.hitbox[0] and man.hitbox[0] < heal.hitbox[0] + heal.hitbox[2]:
                                if consumivel_h.counter < 4:
                                    consumivel_h.counter += 1
                                    heal.heal_visible = False
                                    pygame.display.update()

                # -------------------------------------------------------------------------
                # Função que faz o respawn do consumivel de mana
                # -------------------------------------------------------------------------
                if not mana.mana_visible:
                    mana_respawn += 1
                    if mana_respawn > 250:
                        mana_respawn = 0
                        mana.mana_visible = True

                # -------------------------------------------------------------------------
                # Função que verifica as hitboxes do man em relação a mana se visivel
                # -------------------------------------------------------------------------
                if mana.mana_visible and count_fundo == 0:
                    if man.mana < 60:
                        if man.hitbox[1] < mana.hitbox[1] + mana.hitbox[3] and man.hitbox[1] + man.hitbox[3] > mana.hitbox[1]:
                            if man.hitbox[0] + man.hitbox[2] > mana.hitbox[0] and man.hitbox[0] < mana.hitbox[0] + mana.hitbox[2]:
                                #manasound.play()
                                mana.replenish_mana()

                    # -------------------------------------------------------------------------
                    # Função para coletar e armazenar um coletavel de mana
                    # -------------------------------------------------------------------------
                    elif man.mana >= 60:
                        if man.hitbox[1] < mana.hitbox[1] + mana.hitbox[3] and man.hitbox[1] + man.hitbox[3] > mana.hitbox[1]:
                            if man.hitbox[0] + man.hitbox[2] > mana.hitbox[0] and man.hitbox[0] < mana.hitbox[0] + mana.hitbox[2]:
                                if consumivel_m.counter < 4:
                                    consumivel_m.counter += 1
                                    mana.mana_visible = False
                                    pygame.display.update()

                clock.tick(27)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                # -------------------------------------------------------------------------
                # Função que verifica a hitbox do goblin em relação ao pitchfork
                # -------------------------------------------------------------------------
                for bullet in bullets:
                    if goblin.visible:
                        if goblin.hitbox[1] + goblin.hitbox[3] > bullet.y > goblin.hitbox[1]:
                            if bullet.x + 100 > goblin.hitbox[0] and bullet.x - 100 < goblin.hitbox[0] + goblin.hitbox[2]:
                                hitsound.play()
                                goblin.hit_pitchfork()
                                score += 5
                                bullets.pop(bullets.index(bullet))

                for bullet in bullets:
                    if goblin2.visible:
                        if goblin2.hitbox[1] + goblin2.hitbox[3] > bullet.y > goblin2.hitbox[1]:
                            if bullet.x + 100 > goblin2.hitbox[0] and bullet.x - 100 < goblin2.hitbox[0] + goblin2.hitbox[2]:
                                hitsound.play()
                                goblin2.hit_pitchfork()
                                score += 5
                                bullets.pop(bullets.index(bullet))

                for bullet in bullets:
                    if bloodboss.visible:
                        if bloodboss.hitbox[1] + bloodboss.hitbox[3] > bullet.y > bloodboss.hitbox[1]:
                            if bullet.x + 100 > bloodboss.hitbox[0] and bullet.x - 100 < bloodboss.hitbox[0] + bloodboss.hitbox[2]:
                                hitsound.play()
                                bloodboss.hit_pitchfork()
                                score += 5
                                bullets.pop(bullets.index(bullet))
                    # -------------------------------------------------------------------------
                    # Função para remover o pitchfork do vetor e para mover ele
                    # -------------------------------------------------------------------------
                    if (camera_decente.hitbox[2] - 800) < bullet.x < camera_decente.hitbox[2]:
                        bullet.x += bullet.vel
                    else:
                        bullets.pop(bullets.index(bullet))

                # -------------------------------------------------------------------------
                # Função que verifica a hitbox do goblin em relação ao axe
                # -------------------------------------------------------------------------
                for axe in axes:
                    if goblin.visible:
                        if goblin.hitbox[1] + goblin.hitbox[3] > axe.y > goblin.hitbox[1]:
                            if axe.x > goblin.hitbox[0] and axe.x - 30 < goblin.hitbox[0] + goblin.hitbox[2]:
                                hitsound.play()
                                goblin.hit_axe()
                                score += 1
                                axes.pop(axes.index(axe))

                for axe in axes:
                    if goblin2.visible:
                        if goblin2.hitbox[1] + goblin2.hitbox[3] > axe.y > goblin2.hitbox[1]:
                            if axe.x > goblin2.hitbox[0] and axe.x - 30 < goblin2.hitbox[0] + goblin2.hitbox[2]:
                                hitsound.play()
                                goblin2.hit_axe()
                                score += 1
                                axes.pop(axes.index(axe))


                for axe in axes:
                    if bloodboss.visible and count_fundo == 3:
                        if bloodboss.hitbox[1] + bloodboss.hitbox[3] > axe.y > bloodboss.hitbox[1]:
                            if axe.x > bloodboss.hitbox[0] and axe.x - 30 < bloodboss.hitbox[0] + bloodboss.hitbox[2]:
                                hitsound.play()
                                bloodboss.hit_axe()
                                score += 1
                                axes.pop(axes.index(axe))

                    # -------------------------------------------------------------------------
                    # Função para remover o axe do vetor e para mover ele
                    # -------------------------------------------------------------------------
                    if (camera_decente.hitbox[2] - 800) < axe.x < camera_decente.hitbox[2]:
                        axe.x += axe.vel
                    else:
                        axes.pop(axes.index(axe))

                # -------------------------------------------------------------------------
                # Função para criar um atraso no tiro
                # -------------------------------------------------------------------------
                if shootloop == 1:
                    shootloop += 1
                elif shootloop == 2:
                    shootloop += 1
                elif shootloop == 3:
                    shootloop += 1
                elif shootloop == 4:
                    shootloop += 1
                elif shootloop == 5:
                    shootloop += 1
                elif shootloop == 6:
                    shootloop += 1
                elif shootloop == 7:
                    shootloop += 1
                elif shootloop == 8:
                    shootloop += 1
                elif shootloop == 9:
                    shootloop += 1
                elif shootloop == 10:
                    shootloop += 1
                elif shootloop == 11:
                    shootloop += 1
                elif shootloop == 12:
                    shootloop = 0

                # -------------------------------------------------------------------------
                # Função que captura as teclas apertadas
                # -------------------------------------------------------------------------
                keys = pygame.key.get_pressed()

                # -------------------------------------------------------------------------
                # Função para disparar um axe
                # -------------------------------------------------------------------------
                if keys[pygame.K_z] and man.stamina >= man.staminacoust and shootloop == 0:
                    if man.left:
                        facing = -1
                    else:
                        facing = 1
                    if man.stamina >= man.staminacoust:
                        axes.append(atk(round(man.x + man.W//2) + 5, round(man.y + man.H//2) - 10, facing, 41, 32))
                        man.stamina -= man.staminacoust
                        shootloop = 1

                # -------------------------------------------------------------------------
                # Função para usar o consumivel de cura
                # -------------------------------------------------------------------------
                elif keys[pygame.K_c] and consumivel_h.counter >= 1 and man.health < 250 and shootloop == 0:
                    consumivel_h.heal()

                # -------------------------------------------------------------------------
                # Função para usar o consumivel de mana
                # -------------------------------------------------------------------------
                elif keys[pygame.K_v] and consumivel_m.counter >= 1 and man.mana < 60 and shootloop == 0:
                    consumivel_m.replenish()

                # -------------------------------------------------------------------------
                # Função para disparar o pitchfork
                # -------------------------------------------------------------------------
                if keys[pygame.K_x] and man.mana >= man.manacoust and shootloop == 0:

                    if man.left:
                        facing = -1
                    else:
                        facing = 1
                    if man.mana >= 10:
                        bullets.append(projectile(round(man.x + man.W//2), round(man.y + man.H//2), facing, 113,15))
                        man.mana -= man.manacoust
                        shootloop = 1

                # -------------------------------------------------------------------------
                # Função para andar para esquerda
                # -------------------------------------------------------------------------
                if keys[pygame.K_LEFT]:
                    man.x -= man.vel
                    man.left = True
                    man.right = False
                    man.standing = False

                # -------------------------------------------------------------------------
                # Função de andar para direita
                # -------------------------------------------------------------------------
                elif keys[pygame.K_RIGHT]:
                    man.x += man.vel
                    man.left = False
                    man.right = True
                    man.standing = False

                # -------------------------------------------------------------------------
                # Função de voltar ao menu
                # -------------------------------------------------------------------------
                elif keys[pygame.K_ESCAPE]:
                    if __name__ == '__main__':
                        main()
                else:
                    man.standing = True
                    man.walkCount = 0

                # -------------------------------------------------------------------------
                # Função de pulo
                # -------------------------------------------------------------------------
                if not man.isJump:
                    if keys[pygame.K_SPACE] and man.stamina >= man.staminacoust or keys[pygame.K_UP] and man.stamina >= man.staminacoust:
                        man.isJump = True
                        man.stamina -= man.staminacoust
                        man.left = False
                        man.right = False
                        man.walkCount = 0
                else:
                    if man.jumpCount >= -10:
                        man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
                        man.jumpCount -= 1
                    else:
                        man.jumpCount = 10
                        man.isJump = False

                redrawgamewindow()
            pygame.quit()

        if test:
            break

def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)

def main(test=False):
    """
    Main program.
    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globais
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # -------------------------------------------------------------------------
    # Create pygame screen and objects
    # -------------------------------------------------------------------------
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Player 94")
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Play menu
    # -------------------------------------------------------------------------
    play_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=0,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(H * 0.7),
                                menu_width=int(W * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Menu de Jogo',
                                window_height=H,
                                window_width=W
                                )

    # -------------------------------------------------------------------------
    # Main menu
    # -------------------------------------------------------------------------
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=0,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(H * 0.6),
                                menu_width=int(W * 0.6),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='A Lenda de Kleber',
                                window_height=H,
                                window_width=W
                                )

    main_menu.add_option('Jogar', play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))
    main_menu.add_option('Sair', pygameMenu.events.EXIT)

    # -------------------------------------------------------------------------
    # Configure main menu
    # -------------------------------------------------------------------------
    main_menu.set_fps(FPS)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # -------------------------------------------------------------------------
        # Tick
        # -------------------------------------------------------------------------
        clock.tick(FPS)

        # -------------------------------------------------------------------------
        # Paint background
        # -------------------------------------------------------------------------
        main_background()

        # -------------------------------------------------------------------------
        # Application events
        # -------------------------------------------------------------------------
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # -------------------------------------------------------------------------
        # Main menu
        # -------------------------------------------------------------------------
        main_menu.mainloop(events, disable_loop=test)

        # -------------------------------------------------------------------------
        # Flip surface
        # -------------------------------------------------------------------------
        pygame.display.flip()

        # -------------------------------------------------------------------------
        # At first loop returns
        # -------------------------------------------------------------------------
        if test:
            break
if __name__ == '__main__':
    main()