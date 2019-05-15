import pygame

LARGURA = 640
ALTURA = 480
FPS = 30

# Definir cores
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Inicializa o modulo pygame e cria a tela do jogo
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.left = 10
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        self.speedx = 9
        if keystate[pygame.K_UP]:
            self.speedy = -9
        if keystate[pygame.K_DOWN]:
            self.speedy = 9
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect()
        self.rect.centery = ALTURA / 2
        self.rect.right = LARGURA - 10
        self.veloc_y = 7
    def update(self):
        self.rect.y += self.veloc_y
        if self.rect.bottom > ALTURA:
            self.veloc_y = -9
        if self.rect.top < 0:
            self.veloc_y = 9

game_sprites = pygame.sprite.Group()
player = Player()
boss = Boss()
game_sprites.add(player)
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
    

