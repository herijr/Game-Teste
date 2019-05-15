import pygame

LARGURA = 360
ALTURA = 480
FPS = 30

# Definir cores
PRETO = (0, 0, 0)

# Inicializa o modulo pygame e cria a tela do jogo
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock()

game_sprites = pygame.sprite.Group()

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
    

