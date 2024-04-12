import pygame
import sys
import random
from pygame.locals import *

# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_GRADE = 20  # Definindo o tamanho do grid

# Cores
BRANCO = (255, 255, 255)
AZUL_CEU = (0, 102, 204)  # Azul escuro
VERDE_GRAMA = (0, 102, 0)  # Verde escuro
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)

# Direções
CIMA = (0, -TAMANHO_GRADE)
BAIXO = (0, TAMANHO_GRADE)
ESQUERDA = (-TAMANHO_GRADE, 0)
DIREITA = (TAMANHO_GRADE, 0)

def reiniciar_jogo():
    cobra = [(200, 200), (210, 200), (220, 200)]
    direcao_cobra = DIREITA
    posicao_maca = gerar_posicao_comida(cobra)
    pontuacao = 0
    velocidade = 8  # Velocidade inicial da cobra
    bombas = []
    return cobra, direcao_cobra, posicao_maca, pontuacao, velocidade, bombas

def gerar_posicao_comida(cobra):
    while True:
        posicao = (random.randint(0, (LARGURA_TELA-TAMANHO_GRADE)//TAMANHO_GRADE) * TAMANHO_GRADE,
                   random.randint(0, (ALTURA_TELA-TAMANHO_GRADE)//TAMANHO_GRADE) * TAMANHO_GRADE)
        if posicao not in cobra:
            return posicao

def gerar_bombas(cobra, bombas, pontuacao):
    if pontuacao >= 10:
        num_bombas = min(pontuacao // 10 + 2, 8)  # Começa com 2 bombas e aumenta a cada 10 pontos, com máximo de 8 bombas
        bombas.clear()
        for _ in range(num_bombas):
            posicao = gerar_posicao_comida(cobra)
            bombas.append(posicao)

def jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Snake')

    relogio = pygame.time.Clock()

    imagem_cobra = pygame.Surface((TAMANHO_GRADE, TAMANHO_GRADE))
    imagem_cobra.fill((0, 128, 0))  # Verde escuro

    imagem_maca = pygame.Surface((TAMANHO_GRADE, TAMANHO_GRADE))
    imagem_maca.fill((255, 0, 0))  # Vermelho

    imagem_bomba = pygame.Surface((TAMANHO_GRADE, TAMANHO_GRADE))
    imagem_bomba.fill((0, 0, 255))  # Azul

    cobra, direcao_cobra, posicao_maca, pontuacao, velocidade, bombas = reiniciar_jogo()

    fim_de_jogo = False
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == K_UP or evento.key == K_w:
                    if direcao_cobra != BAIXO:
                        direcao_cobra = CIMA
                elif evento.key == K_DOWN or evento.key == K_s:
                    if direcao_cobra != CIMA:
                        direcao_cobra = BAIXO
                elif evento.key == K_LEFT or evento.key == K_a:
                    if direcao_cobra != DIREITA:
                        direcao_cobra = ESQUERDA
                elif evento.key == K_RIGHT or evento.key == K_d:
                    if direcao_cobra != ESQUERDA:
                        direcao_cobra = DIREITA
                elif evento.key == K_r and fim_de_jogo:
                    cobra, direcao_cobra, posicao_maca, pontuacao, velocidade, bombas = reiniciar_jogo()
                    fim_de_jogo = False

        if fim_de_jogo:
            fonte = pygame.font.SysFont(None, 36)
            texto = fonte.render('Fim de Jogo - Pontuação: {}'.format(pontuacao), True, VERMELHO)
            rect_texto = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto, rect_texto)
            pygame.display.update()
            continue

        nova_cabeca = (cobra[0][0] + direcao_cobra[0], cobra[0][1] + direcao_cobra[1])
        cobra.insert(0, nova_cabeca)

        if cobra[0] == posicao_maca:
            posicao_maca = gerar_posicao_comida(cobra)
            pontuacao += 1
            gerar_bombas(cobra, bombas, pontuacao)
            velocidade += 0.3  # Aumenta a velocidade gradualmente
        else:
            cobra.pop()

        for bomba in bombas:
            if cobra[0] == bomba:
                fim_de_jogo = True

        if (cobra[0][0] < 0 or cobra[0][0] >= LARGURA_TELA or
                cobra[0][1] < 0 or cobra[0][1] >= ALTURA_TELA or
                cobra[0] in cobra[1:]):
            fim_de_jogo = True

        tela.fill(AZUL_CEU)
        pygame.draw.rect(tela, VERDE_GRAMA, (0, ALTURA_TELA // 2, LARGURA_TELA, ALTURA_TELA // 2))
        for posicao in cobra:
            tela.blit(imagem_cobra, posicao)
        tela.blit(imagem_maca, posicao_maca)
        for bomba in bombas:
            tela.blit(imagem_bomba, bomba)

        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render('Pontuação: {}'.format(pontuacao), True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))

        pygame.display.update()

        relogio.tick(velocidade)  # Ajuste para rodar com a velocidade atual

if __name__ == '__main__':
    jogo()
