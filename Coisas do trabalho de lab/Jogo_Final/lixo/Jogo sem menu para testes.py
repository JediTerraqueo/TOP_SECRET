import pygame
from pygame import *
import random
import pygame
from pygame import *
import random
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
platform_spacing = 100
W = 800
H = 600
win = pygame.display.set_mode((W, H))
info = {
    'screen_y': 0,
    'score': 0,
    'high_score': 0
}
music = pygame.mixer.music.load('Fundo começo do mapa.mp3')
pygame.mixer.music.play(-1)

clock = None
main_menu = None
surface = None

while True:



   win = pygame.display.set_mode((W, H))
   pygame.display.set_caption("Tapa Buraco")
   walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                    pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                    pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
   walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                   pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                   pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
   atk_left = [pygame.image.load('machado_1.1_left.png'), pygame.image.load('machado_1.2_left.png'),
                   pygame.image.load('machado_1.3_left.png'), pygame.image.load('machado_1.4_left.png')]
   atk_right = [pygame.image.load('machado_2.1_right.png'), pygame.image.load('machado_2.2_right.png'),
                    pygame.image.load('machado_2.3_right.png'), pygame.image.load('machado_2.4_right.png')]
   hitsound = pygame.mixer.Sound('hit.wav')
   man_hitsound = pygame.mixer.Sound('efeito de quando toma um dano.wav')
   man_hitsound_2 = pygame.mixer.Sound('efeito de quando toma um dano_2.wav')
   healsound = pygame.mixer.Sound('craocraocrao.wav')
   clock = pygame.time.Clock()
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
                       pygame.quit()
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

   class Platform_Manager:
       def __init__(self):
           self.platforms = []
           self.spawns = 0
           self.start_spawn = W

           scale = 3
           self.width, self.height = 24 * scale, 6 * scale

       def update(self):
           self.spawner()
           return self.manage()

       def spawner(self):
           if H - info['screen_y'] > self.spawns * platform_spacing:
               self.spawn()

       def spawn(self):
           y = self.start_spawn - self.spawns * platform_spacing
           x = random.randint(-self.width, W)

           self.platforms.append(Platform(x,y,random.choice([1,-1])))
           self.spawns += 1

       def manage(self):
           u = []
           b = []
           for i in self.platforms:
               b.append(i.show())

               if i.on_screen():
                   u.append(i)

           self.platforms = u
           return b

   class Platform:
       def __init__(self,x,y,direction):
           self.x = x
           self.y = y
           self.direction = direction
           self.speed = 2
           self.colour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
           scale = 3
           self.width  = 24 * scale
           self.height = 6 * scale

       def on_screen(self):
           if self.y > info['screen_y'] + H:
               return False
           return True

       def show(self):
           return ((0,0,0), (self.x, self.y, self.width, self.height))

   def random_colour(l,h):
       return (random.randint(l,h),random.randint(l,h),random.randint(l,h))

   def blit_images(x):
       for i in x:
           window.blit(transform.scale(i[0], (i[1][2],i[1][3])), (i[1][0], i[1][1] - info['screen_y']))

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
       resurection = [pygame.image.load('fase-1.png'), pygame.image.load('fase-2.png'), pygame.image.load('fase-3.png'),
                      pygame.image.load('fase-4.png'), pygame.image.load('fase-5.png'), pygame.image.load('fase-6.png'),
                      pygame.image.load('fase-7.png'), pygame.image.load('fase-8.png'), pygame.image.load('fase-9.png'),
                      pygame.image.load('fase-10.png'), pygame.image.load('fase-11.png'), pygame.image.load('fase-12.png'),
                      pygame.image.load('fase-13.png'), pygame.image.load('fase-14.png'), pygame.image.load('fase-15.png'),
                      pygame.image.load('fase-16.png'), pygame.image.load('fase-17.png'), pygame.image.load('fase-18.png')]

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
       Mana = pygame.image.load('mana_flask.png')
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
               self.rel_x = self.mana_x % fundo.bg.get_rect().width - 600

               if self.rel_x < W + 1000:
                   self.hitbox = (self.rel_x + 400, self.mana_y, self.width, self.height)
                   win.blit(self.Mana, (self.rel_x - (self.Mana.get_rect().width - 422), 400))

               self.mana_x -= 2
               pygame.draw.rect(win, (255,0,0), self.hitbox,2)
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
       heart = pygame.image.load('health_flask.png')
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
               self.rel_x = self.heal_x % fundo.bg.get_rect().width - 600

               if self.rel_x < W + 1000:
                   self.hitbox = (self.rel_x + 400, self.heal_y, self.width, self.height)
                   win.blit(self.heart, (self.rel_x - (self.heart.get_rect().width - 423), 400))

               self.heal_x -= 2
               pygame.draw.rect(win, (255,0,0), self.hitbox,2)
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
       parallax = pygame.image.load('fundo parallax.png')
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
       bg = pygame.image.load('Teste de fundo longo.png')
       def __init__(self, x, y, w, h, rel_x):
           self.x = x
           self.y = y
           self.width = w
           self.height = h
           self.rel_x = rel_x

       # -------------------------------------------------------------------------
       # Funçao que desenha o fundo
       # -------------------------------------------------------------------------
       def draw(self, win):
           self.rel_x = self.x % fundo.bg.get_rect().width
           win.blit(self.bg, (self.rel_x - self.bg.get_rect().width, 0))
           if self.rel_x < W:
               win.blit(self.bg, (self.rel_x, 0))
           self.x -= 2

   # -------------------------------------------------------------------------
   # Classe do consumivel de cura
   # -------------------------------------------------------------------------
   class consumivel_health(object):
       consumivel_1 = pygame.image.load('consumivel_1.png')
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
       consumivel_2 = pygame.image.load('consumivel_2.png')
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
       hud = pygame.image.load('Hud basico.png')
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
       plataformer = pygame.image.load('plataforma.png')
       def __init__(self, x, y, w, h, rel_x):
           self.x = x
           self.y = y
           self.w = w
           self.h = h
           self.rel_x = rel_x
           self.hitbox = (self.rel_x + 400, self.y, w, h)

       # -------------------------------------------------------------------------
       # Função que desenha a plataforma na tela
       # -------------------------------------------------------------------------
       def draw(self, win):

           self.rel_x = self.x % fundo.bg.get_rect().width - 600

           if self.rel_x < W + 1000:
               self.hitbox = (self.rel_x + 400, self.y, self.w, self.h)
               win.blit(self.plataformer, (self.rel_x - (self.plataformer.get_rect().width - 570), 400))

           self.x -= 2
           pygame.draw.rect(win, (255,0,0), self.hitbox,2)

   class camera_decente(object):
       def __init__(self, x, y, w, h):
           self.x = x
           self.y = y
           self.w = w
           self.h = h
           self.hitbox = (self.x, self.y, w, h)

       def draw(self, win):
           pygame.draw.rect(win, (255,0,0), self.hitbox,2)

   # -------------------------------------------------------------------------
   # Função que desenha as imagens na tela
   # -------------------------------------------------------------------------
   def redrawgamewindow():
       #parallax.draw(win)
       #fundo.draw(win)
       win.fill((0,0,0))
       for x in platform_blit:
           i = list(x)
           i[1] = list(i[1])
           i[1][1] -= info['screen_y']
           draw.rect(win, i[0], i[1])
       camera_decente.draw(win)
       text = font.render('Score: '+ str(score), 1, (255,255,255))
       text_1 = font_1.render(str(consumivel_h.counter), 1, (255,255,255))
       text_2 = font_1.render(str(consumivel_m.counter), 1, (255,255,255))
       text_c = font_2.render('C', 1, (255,255,255))
       text_v = font_2.render('V', 1, (255,255,255))
       heal.draw(win)
       mana.draw(win)
       man.draw(win)
       goblin.draw(win)
       hud.draw(win)
       plataforma.draw(win)
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
   font = pygame.font.SysFont('comicsans', 30, True)
   font_1 = pygame.font.SysFont('comicsans', 30, True)
   font_2 = pygame.font.SysFont('comicsans', 25, True)
   man = player(10, 485, 64, 64)
   goblin = enemy(100, 490, 64, 64, 450)
   heal = Cure(300, 400, 22, 55, 0)
   mana = Mana(200, 400, 22, 54, 0)
   parallax = parallax(0, 0, 1600, 600, 0)
   fundo = fundo(0, 0, 1600, 600, 0)
   plataforma = plataforma(400, 400, 170, 66, 0)
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

   # -------------------------------------------------------------------------
   # main loop
   # -------------------------------------------------------------------------
   while run:
       while run:
           while True:
               #MATH THINGS
               #   event_loop()
               platform_blit = platform_manager.update()
               #   clock.tick(60)
               #DISPLAY THINGS
               win.fill((255,255,255))
           # -------------------------------------------------------------------------
           # Função que verifica as hitboxes do goblin em relação a plataforma
           # -------------------------------------------------------------------------
           if goblin.visible:
               if goblin.hitbox[1] < plataforma.hitbox[1] + plataforma.hitbox[3] and goblin.hitbox[1] + goblin.hitbox[3] > plataforma.hitbox[1]:
                   if goblin.hitbox[0] + goblin.hitbox[2] > plataforma.hitbox[0] and goblin.hitbox[0] < plataforma.hitbox[0] + plataforma.hitbox[2]:
                       goblin.y = plataforma.y - 55
                       if goblin.y < plataforma.y - 55:
                           goblin.y -= 25
                   else:
                       if not goblin.isjump:
                           goblin.y += 25
               elif goblin.y < 480 and not goblin.isjump:
                   goblin.y += 25

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


           # -------------------------------------------------------------------------
           # Função que faz o respawn do consumivel de cura
           # -------------------------------------------------------------------------
           if not heal.heal_visible:
               heal_respawn += 1
               if heal_respawn > 250:
                   heal_respawn = 0
                   heal.heal_visible = True

           # -------------------------------------------------------------------------
           # Função que verifica as hitboxes do man em relação a cura se visivel
           # -------------------------------------------------------------------------
           if heal.heal_visible:
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
           if mana.mana_visible:
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
           if keys[pygame.K_z] and man.stamina >= 20 and shootloop == 0:
               if man.left:
                   facing = -1
               else:
                   facing = 1
               if man.stamina >= 20:
                   axes.append(atk(round(man.x + man.W//2) + 5, round(man.y + man.H//2) - 10, facing, 41, 32))
                   man.stamina -= 25
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
           if keys[pygame.K_x] and man.mana >= 20 and shootloop == 0:

               if man.left:
                   facing = -1
               else:
                   facing = 1
               if man.mana >= 10:
                   bullets.append(projectile(round(man.x + man.W//2), round(man.y + man.H//2), facing, 113,15))
                   man.mana -= 10
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

           elif keys[pygame.K_ESCAPE]:
               if __name__ == '__main__':
                   pass
           else:
               man.standing = True
               man.walkCount = 0

           # -------------------------------------------------------------------------
           # Função de pulo
           # -------------------------------------------------------------------------
           if not man.isJump:
               if keys[pygame.K_SPACE] and man.stamina >= 50 or keys[pygame.K_UP] and man.stamina >= 50:
                   man.isJump = True
                   man.stamina -= 50
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