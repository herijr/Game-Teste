import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

LARGURA = 640
ALTURA = 480
FPS = 30

# Definir cores
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Inicializa o modulo pygame e cria a tela do jogo
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock()

def vida_chefe(surf, x, y, pct):
    if pct < 0:
        pct = 0
    COMPRIMENTO_BARRA = 200
    ALTURA_BARRA = 10
    nivel_vida = (pct * 0.01) * COMPRIMENTO_BARRA
    linha_fora = pygame.Rect(x, y, COMPRIMENTO_BARRA, ALTURA_BARRA)
    preench = pygame.Rect(x, y, nivel_vida, ALTURA_BARRA)
    pygame.draw.rect(surf, VERMELHO, preench)
    pygame.draw.rect(surf, BRANCO, linha_fora, 2)

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(jogador_img, (38, 50))
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = 10
        self.veloc_y = 0
        self.veloc_x = 0
        self.tiro_intervalo = 250
        self.vidas = 5
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        self.veloc_y = 0
        self.veloc_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.veloc_y = -9
        if keystate[pygame.K_DOWN]:
            self.veloc_y = 9
        if keystate[pygame.K_LEFT]:
            self.veloc_x = -9
        if keystate[pygame.K_RIGHT]:
            self.veloc_x = 9
        if keystate[pygame.K_SPACE]:            
            self.atirar()
        self.rect.y += self.veloc_y
        self.rect.x += self.veloc_x
        if self.rect.top < 25:
            self.rect.top = 25
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.tiro_intervalo:
            self.ultimo_tiro = agora
            tiro = Tiro(self.rect.centery, self.rect.right)
            game_sprites.add(tiro)
            tiros.add(tiro)

class Chefe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = chefe_img
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.centery = ALTURA / 2
        self.rect.right = LARGURA - 10
        self.veloc_y = 7
        self.vida = 100
        self.tiro_intervalo = 500
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.veloc_y
        self.atirar()
        if self.rect.bottom > ALTURA:
            self.veloc_y = -9
        if self.rect.top < 0:
            self.veloc_y = 9
    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.tiro_intervalo:
            self.ultimo_tiro = agora
            tiroinimigo = Tiroinimigo(self.rect.centery, self.rect.left)
            game_sprites.add(tiroinimigo)
            tirosinimigo.add(tiroinimigo)

class Tiro(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = tiro_img
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.left =  x
        self.rect.centery = y
        self.speedx = 10
    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > LARGURA:
            self.kill()

class Tiroinimigo(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = tiroinimigo_img
        self.image.set_colorkey(PRETO)
        self.rect = self.image.get_rect()
        self.rect.right =  x
        self.rect.centery = y
        self.speedx = -10
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

# Carrega Imagens do jogo
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
chefe_img = pygame.image.load(path.join(img_dir, "img_chefe.png")).convert()
jogador_img = pygame.image.load(path.join(img_dir, "img_jogador.png")).convert()
tiro_img = pygame.image.load(path.join(img_dir, "tiro.png")).convert()
tiroinimigo_img = pygame.image.load(path.join(img_dir, "tiroinimigo.png")).convert()

game_sprites = pygame.sprite.Group()
tiros = pygame.sprite.Group()
tirosinimigo = pygame.sprite.Group()
jogador = Jogador()
chefe = Chefe()
chefes = pygame.sprite.Group()
game_sprites.add(jogador)
chefes.add(chefe)
game_sprites.add(chefe)

# Game Loop
rodando = True

while rodando:
    # Mantem o loop do jogo na velocidade correta
    clock.tick(FPS)
    # eventos e inputs no jogo
    for event in pygame.event.get():
        # verifica se a janela foi fechada
        if event.type == pygame.QUIT:
            rodando = False
            
    # Update
    game_sprites.update()
    # se um tiro acerta o inimigo
    hits = pygame.sprite.groupcollide(tiros, chefes, True, False)
    for hit in hits:
        chefe.vida -= 5
        if chefe.vida <= 0:
            rodando = False

    # se um tiro inimigo acerta o jogador
    hits2 = pygame.sprite.spritecollide(jogador, tirosinimigo, True)
    for hit in hits2:
        jogador.vidas -= 1
        if jogador.vidas <= 0:
            rodando = False
            
    # Render / Draw
    tela.fill(PRETO)
    tela.blit(background, background_rect)

    game_sprites.draw(tela)
    vida_chefe(tela, 5, 5, chefe.vida)
    # flip display, apos renderizar itens
    pygame.display.flip()

pygame.quit()
