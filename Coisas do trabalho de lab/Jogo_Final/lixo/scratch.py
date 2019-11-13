import pygame
import sys
import os
from random import randrange
import pygameMenu
from pygame.locals import *

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
X = 0
music = pygame.mixer.music.load('Fundo começo do mapa.mp3')
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
    pos_x = 0
    pos_y = 270
    x = -310
    y = -210
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
        walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                     pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                     pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
        walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                    pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                    pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
        bg = pygame.image.load('Fundo em 8 bits_3.png')
        parallax = pygame.image.load('fundo_ceu_final.png')
        clock = pygame.time.Clock()
        hitsound = pygame.mixer.Sound('hit.wav')
        man_hitsound = pygame.mixer.Sound('efeito de quando toma um dano.wav')
        man_hitsound_2 = pygame.mixer.Sound('efeito de quando toma um dano_2.wav')
        healsound = pygame.mixer.Sound('craocraocrao.wav')
        score = 0

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

                pygame.draw.rect(win, (168,168,168), (10, 20, 250, 10))
                pygame.draw.rect(win, (255,0,0), (10, 20, 50 - (50 - self.health), 10))
                pygame.draw.rect(win, (168,168,168), (10, 40, 100, 10))
                pygame.draw.rect(win, (0,255,0), (10, 40, 100 - (100 - self.stamina), 10))
                pygame.draw.rect(win, (168,168,168), (10, 60, 50, 10))
                pygame.draw.rect(win, (0,0,255), (10, 60, 100 - (110 - self.mana), 10))
                self.hitbox = (self.x + 17, self.y + 11 , 29, 52)

            # -------------------------------------------------------------------------
            # Função que mostra quando algo acerta o player
            # -------------------------------------------------------------------------
            def hit(self):

                if self.health > 0:
                    self.health -= 50
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

                    self.x = 10
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
            walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                         pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                         pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                         pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
            walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                        pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                        pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                        pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
            colision = [pygame.image.load('explosão_1.png'), pygame.image.load('explosão_2.png'), pygame.image.load('explosão_3.png'),
                        pygame.image.load('explosão_4.png'), pygame.image.load('explosão_5.png'), pygame.image.load('explosão_6.png')]

            def __init__(self, x ,y, W, H, end):
                self.x = x
                self.y = y
                self.W = W
                self.H = H
                self.end = end
                self.path = [self.x, self.y]
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

            def draw(self,win):
                self.move()
                if self.visible:
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
                    if self.time + 1 <= 18:
                        win.blit(self.colision[self.time // 3], (self.x, self.y - 55))
                        self.time += 1

            # -------------------------------------------------------------------------
            # Função para movimentar o inimigo
            # -------------------------------------------------------------------------
            def move(self):
                if self.escolha:
                    if not (goblin.isjump):
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


        # -------------------------------------------------------------------------
        # Classes a parte
        # -------------------------------------------------------------------------
        class atk(object):
            atk_left = [pygame.image.load('machado_1_left.png'), pygame.image.load('machado_2_left.png'),
                        pygame.image.load('machado_3_left.png'), pygame.image.load('machado_4_left.png')]

            atk_right = [pygame.image.load('machado_1_right.png'), pygame.image.load('machado_2_right.png'),
                         pygame.image.load('machado_3_right.png'), pygame.image.load('machado_4_right.png')]

            def __init__(self, x, y, facing, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h
                self.facing = facing
                self.vel = 8 * facing
                self.hitbox = (self.x, self.y, w, h)
                self.spins = 0


            def draw(self,win):
                if self.spins + 1 >= 16:
                    self.spins = 0

                    if man.left:
                        while axe.x > 0 and axe.x < 800:
                            win.blit(atk_right[self.spins // 2], (self.x, self.y))
                            self.spins += 1

                    elif man.right:
                        while axe.x > 0 and axe.x < 800:
                            win.blit(atk_left[self.spins // 2], (self.x, self.y))
                            self.spins += 1

        class projectile(object):
            pitchfork_right = pygame.image.load('pitchfork_right.png')
            pitchfork_left = pygame.image.load('pitchfork_left.png')
            def __init__(self, x, y, facing, w, h):
                self.x = x
                self.y = y
                self.width = w
                self.height = h
                self.facing = facing
                self.vel = 12 * facing
                self.hitbox = (self.x, self.y, w, h)

            def draw(self,win):
                if facing == 1:
                    win.blit(self.pitchfork_right, (self.x, self.y))
                elif facing == -1:
                    win.blit(self.pitchfork_left, (self.x - 120, self.y))

        class Mana(object):
            Mana = pygame.image.load('pilula azul.png')
            def __init__(self, x ,y, w, h):
                self.mana_visible = True
                self.mana_x = x
                self.mana_y = y
                self.width = w
                self.height = h
                self.hitbox = (self.mana_x, self.mana_y, w, h)

            def draw(self, win):
                if mana.mana_visible:
                    win.blit(self.Mana, (self.mana_x, self.mana_y))
                    #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

            def replenish_mana(self):
                man.mana += 10
                mana.mana_visible = False
                pygame.display.update()

        class Cure(object):
            heart = pygame.image.load('coração_3.png')
            def __init__(self, x, y, w, h):
                self.heal_visible = True
                self.heal_x = x
                self.heal_y = y
                self.width = w
                self.height = h
                self.hitbox = (self.heal_x, self.heal_y, w, h)

            def draw(self, win):
                if heal.heal_visible:
                    win.blit(self.heart, (self.heal_x, self.heal_y))
                    #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

            def cure(self):
                man.health += 50
                heal.heal_visible = False
                pygame.display.update()

        # -------------------------------------------------------------------------
        # Função que desenha as imagens na tela
        # -------------------------------------------------------------------------
        def redrawgamewindow():
            global X
            rel_x = X % bg.get_rect().width
            win.blit(parallax, (rel_x - parallax.get_rect().width, 0))
            if rel_x < W:
                win.blit(parallax, (rel_x, 0))
            X -= 1
            win.blit(bg, (0, 0))
            text = font.render('Score: '+ str(score), 1, (255,255,255))
            heal.draw(win)
            mana.draw(win)
            man.draw(win)
            goblin.draw(win)
            win.blit(text, (650,25))
            for bullet in bullets:
                bullet.draw(win)

            pygame.display.update()

        # -------------------------------------------------------------------------
        #main loop
        # -------------------------------------------------------------------------
        font = pygame.font.SysFont('comicsans', 30, True)
        man = player(10, 485, 64, 64)
        goblin = enemy(100, 490, 64, 64, 450)
        heal = Cure(300, 400, 39, 37)
        mana = Mana(200, 400, 62, 28)
        run = True
        bullets = []
        axes = []
        respawn = 0
        heal_respawn = 0
        mana_respawn = 0
        shootloop = 0
        shootloop_a = 0

        while run:
            while run:
                if man.stamina < 100:
                    man.timer += 1
                    if man.timer >= 20:
                        man.stamina += 2
                elif man.stamina == 100:
                    man.timer = 0
                if goblin.visible == False:
                    respawn += 1
                    if respawn > 100:
                        respawn = 0
                        goblin.visible = True
                        goblin.escolha = True
                        goblin.health = 10

                if goblin.visible == True:
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

                if heal.heal_visible == False:
                    heal_respawn += 1
                    if heal_respawn > 250:
                        heal_respawn = 0
                        heal.heal_visible = True

                if heal.heal_visible:
                    if man.health < 250:
                        if man.hitbox[1] < heal.hitbox[1] + heal.hitbox[3] and man.hitbox[1] + man.hitbox[3] > heal.hitbox[1]:
                            if man.hitbox[0] + man.hitbox[2] > heal.hitbox[0] and man.hitbox[0] < heal.hitbox[0] + heal.hitbox[2]:
                                healsound.play()
                                heal.cure()


                if mana.mana_visible == False:
                    mana_respawn += 1
                    if mana_respawn > 250:
                        mana_respawn = 0
                        mana.mana_visible = True

                if mana.mana_visible:
                    if man.mana < 60:
                        if man.hitbox[1] < mana.hitbox[1] + mana.hitbox[3] and man.hitbox[1] + man.hitbox[3] > mana.hitbox[1]:
                            if man.hitbox[0] + man.hitbox[2] > mana.hitbox[0] and man.hitbox[0] < mana.hitbox[0] + mana.hitbox[2]:
                                #manasound.play()
                                mana.replenish_mana()
                clock.tick(27)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                for bullet in bullets:
                    if goblin.visible == True:
                        if bullet.y < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y > goblin.hitbox[1]:
                            if bullet.x + 100 > goblin.hitbox[0] and bullet.x - 100 < goblin.hitbox[0] + goblin.hitbox[2]:
                                hitsound.play()
                                goblin.hit_pitchfork()
                                score += 1
                                bullets.pop(bullets.index(bullet))

                    if bullet.x < 800 and bullet.x > 0:
                        bullet.x += bullet.vel
                    else:
                        bullets.pop(bullets.index(bullet))

                for axe in axes:
                    if goblin.visible == True:
                        if axe.y < goblin.hitbox[1] + goblin.hitbox[3] and axe.y > goblin.hitbox[1]:
                            if axe.x > goblin.hitbox[0] and axe.x - 100 < goblin.hitbox[0] + goblin.hitbox[2]:
                                hitsound.play()
                                goblin.hit_axe()
                                score += 1
                                axes.pop(axes.index(axe))

                    if axe.x < 800 and axe.x > 0:
                        axe.x += axe.vel
                    else:
                        axes.pop(axes.index(axe))

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

                if shootloop_a == 1:
                    shootloop_a += 1
                elif shootloop_a == 2:
                    shootloop_a += 1
                elif shootloop_a == 3:
                    shootloop_a += 1
                elif shootloop_a == 4:
                    shootloop_a += 1
                elif shootloop_a == 5:
                    shootloop_a += 1
                elif shootloop_a == 6:
                    shootloop_a += 1
                elif shootloop_a == 7:
                    shootloop_a += 1
                elif shootloop_a == 8:
                    shootloop_a += 1
                elif shootloop_a == 8:
                    shootloop_a += 1
                elif shootloop_a == 8:
                    shootloop_a = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_z] and man.stamina >= 20 and shootloop_a == 0:
                    if man.left:
                        facing = -1
                    else:
                        facing = 1
                    if man.stamina >= 20:
                        axes.append(atk(round(man.x + man.W//2), round(man.y + man.H//2), facing, 159, 210))
                        man.stamina -= 10
                        shootloop = 1

                if keys[pygame.K_c]:
                    pass

                if keys[pygame.K_x] and man.mana >= 10 and shootloop == 0:

                    if man.left:
                        facing = -1
                    else:
                        facing = 1
                    if man.mana >= 20:
                        bullets.append(projectile(round(man.x + man.W//2), round(man.y + man.H//2), facing, 113,15))
                        man.mana -= 20
                        shootloop = 1

                if keys[pygame.K_LEFT]:
                    man.x -= man.vel
                    man.left = True
                    man.right = False
                    man.standing = False

                elif keys[pygame.K_RIGHT]:
                    man.x += man.vel
                    man.left = False
                    man.right = True
                    man.standing = False

                elif keys[pygame.K_ESCAPE]:
                    if __name__ == '__main__':
                        main()
                else:
                    man.standing = True
                    man.walkCount = 0

                if not (man.isJump):
                    if keys[pygame.K_SPACE]:
                        man.isJump = True
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
    pygame.display.set_caption("Tapa buraco")
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Cria menus
    # -------------------------------------------------------------------------

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

    play_submenu = pygameMenu.Menu(surface,
                                   bgfun=main_background,
                                   color_selected=COLOR_WHITE,
                                   font=pygameMenu.font.FONT_BEBAS,
                                   font_color=COLOR_BLACK,
                                   font_size=30,
                                   menu_alpha=0,
                                   menu_color=MENU_BACKGROUND_COLOR,
                                   menu_height=int(H * 0.5),
                                   menu_width=int(W * 0.7),
                                   option_shadow=False,
                                   title='Submenu',
                                   window_height=H,
                                   window_width=W
                                   )
    play_submenu.add_option('Back', pygameMenu.events.BACK)

    play_menu.add_option('Jogar',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))
    play_menu.add_selector('Escolha a dificuldade',
                           [('1 - Facil', 'EASY'),
                            ('2 - Medio', 'MEDIUM'),
                            ('3 - Dificil', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add_option('Outro menu', play_submenu)
    play_menu.add_option('Retornar para o menu principal', pygameMenu.events.BACK)

    # -------------------------------------------------------------------------
    # Rank menu
    # -------------------------------------------------------------------------
    rank_menu = pygameMenu.TextMenu(surface,
                                     bgfun=main_background,
                                     color_selected=COLOR_WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     font_size_title=30,
                                     font_title=pygameMenu.font.FONT_8BIT,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_color_title=COLOR_BACKGROUND,
                                     menu_height=int(H * 0.6),
                                     menu_width=int(W * 0.6),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=20,
                                     title='Rank',
                                     window_height=H,
                                     window_width=W
                                     )
    rank_menu.add_option('Back', pygameMenu.events.BACK)
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
                                title='Tapa buraco',
                                window_height=H,
                                window_width=W
                                )

    main_menu.add_option('Jogar', play_menu)
    main_menu.add_option('Rank', rank_menu)
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