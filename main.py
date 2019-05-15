import pygame

LARGURA = 640
ALTURA = 480
FPS = 30

# Definir cores
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Inicializa o modulo pygame e cria a tela do jogo
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock()

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = 10
        self.veloc_y = 0
        self.tiro_intervalo = 250
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        self.veloc_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.veloc_y = -9
        if keystate[pygame.K_DOWN]:
            self.veloc_y = 9
        if keystate[pygame.K_SPACE]:
            self.atirar()
        self.rect.y += self.veloc_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.tiro_intervalo:
            self.ultimo_tiro = agora
            tiro = Tiro(self.rect.centery, self.rect.right)
            game_sprites.add(tiro)
            tiros.add(tiro)

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.centery = ALTURA / 2
        self.rect.right = LARGURA - 10
        self.veloc_y = 7
        self.tiro_intervalo = 800
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
        self.image = pygame.Surface((20, 10))
        self.image.fill(VERDE)
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
        self.image = pygame.Surface((20, 10))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.right =  x
        self.rect.centery = y
        self.speedx = -10
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

game_sprites = pygame.sprite.Group()
tiros = pygame.sprite.Group()
tirosinimigo = pygame.sprite.Group()
jogador = Jogador()
boss = Boss()
game_sprites.add(jogador)
game_sprites.add(boss)

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
    # Render / Draw
    tela.fill(PRETO)
    game_sprites.draw(tela)
    # flip display, apos renderizar itens
    pygame.display.flip()

pygame.quit()
    

