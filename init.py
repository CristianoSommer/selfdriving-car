import datetime
import numpy as np
import random
import pygame
import time
import matplotlib.pyplot as plt
import tkinter
import os.path

from tkinter import messagebox
from deepQLearning import Agente
from ambiente import Ambiente

TAMANHO_CENARIO_X = 10
TAMANHO_CENARIO_Y = 13

def desenharAmbiente(x, y, ambiente, acao, episode, loss):  

    for i in range(0,10):
        for j in range(0,13):
            tamanho_x = i * 100
            tamanho_y = j * 100

            color = (64, 64, 64)
            if ambiente.mapa[i,j] == 0.0:
                color = (66, 117, 40)
            elif ambiente.mapa[i,j] == 0.75:
                color = (74, 89, 88)
            elif ambiente.mapa[i,j] == 0.5:
                color = (10,25,60)
            
            pygame.draw.rect(screen,color,(tamanho_y,tamanho_x,tamanho_y+100,tamanho_x+100),0)


    estrada = pygame.image.load("img/estrada/estrada.png").convert()
    estrada = pygame.transform.scale(estrada, (100, 100))

    estrada_semlinha = pygame.image.load("img/estrada/estrada_semlinha.png").convert()
    estrada_semlinha = pygame.transform.scale(estrada_semlinha, (100, 100))

    screen.blit(estrada_semlinha, (0, 0))

    for linha in [0, 3, 6, 9]:
        for coluna in range(1, TAMANHO_CENARIO_Y):
            if coluna % 4 != 0:
                screen.blit(estrada, (coluna * 100, linha * 100))
            else:
                screen.blit(estrada_semlinha, (coluna * 100, linha * 100))

    estrada = pygame.transform.rotate(estrada, 90)
    estrada_semlinha = pygame.transform.rotate(estrada_semlinha, 90)

    for coluna in [0, 4, 8, 12]:
        for linha in range(1, TAMANHO_CENARIO_X):
            if linha % 3 != 0:
                screen.blit(estrada, (coluna * 100, linha * 100))
            else:
                screen.blit(estrada_semlinha, (coluna * 100, linha * 100))

    arvore = pygame.image.load("img/cidade/arvore.png").convert_alpha() 
    casa = pygame.image.load("img/cidade/casa.png").convert_alpha() 
    ap_pequeno = pygame.image.load("img/cidade/apartamento_pequeno.png").convert_alpha() 
    ap = pygame.image.load("img/cidade/apartamento.png").convert_alpha() 


    screen.blit(estrada_semlinha, (100, 100)) # Origem
    screen.blit(estrada_semlinha, (700, 800)) # Destino

    carro = pygame.image.load("img/carro/{}.png".format(acao)).convert_alpha()  
    screen.blit(carro, (y*100 + 28,x*100 + 25))

    # bloco 1
    screen.blit(casa, (110, 170))
    screen.blit(arvore, (190, 200))
    screen.blit(arvore, (260, 120))
    screen.blit(arvore, (320, 140))
    screen.blit(ap, (300, 200))

    # bloco 2
    screen.blit(ap_pequeno, (550, 120))
    screen.blit(ap_pequeno, (680, 120))
    screen.blit(arvore, (550, 220))
    screen.blit(arvore, (610, 220))
    screen.blit(arvore, (660, 220))
    screen.blit(arvore, (720, 220))

    # bloco 3
    screen.blit(casa, (920, 120))
    screen.blit(casa, (1100, 120))
    screen.blit(arvore, (1025, 125))
    screen.blit(arvore, (1025, 225))
    screen.blit(casa, (920, 220))
    screen.blit(casa, (1100, 220))

    # bloco 4
    screen.blit(ap, (130, 410))
    screen.blit(ap, (250, 500))
    screen.blit(arvore, (250, 400))
    screen.blit(arvore, (270, 420))
    screen.blit(arvore, (240, 435))

    # bloco 5
    screen.blit(arvore, (500, 410))
    screen.blit(arvore, (500, 460))
    screen.blit(arvore, (500, 510))
    screen.blit(arvore, (500, 560))
    screen.blit(arvore, (550, 410))
    screen.blit(arvore, (550, 460))
    screen.blit(arvore, (550, 510))
    screen.blit(arvore, (550, 560))
    screen.blit(arvore, (600, 410))
    screen.blit(arvore, (600, 460))
    screen.blit(arvore, (600, 510))
    screen.blit(arvore, (600, 560))
    screen.blit(arvore, (650, 410))
    screen.blit(arvore, (650, 460))
    screen.blit(arvore, (650, 510))
    screen.blit(arvore, (650, 560))
    screen.blit(arvore, (700, 410))
    screen.blit(arvore, (700, 460))
    screen.blit(arvore, (700, 510))
    screen.blit(arvore, (700, 560))
    screen.blit(arvore, (750, 410))
    screen.blit(arvore, (750, 460))
    screen.blit(arvore, (750, 510))
    screen.blit(arvore, (750, 560))
    

    #bloco 6
    screen.blit(casa, (920, 420))
    screen.blit(casa, (920, 520))
    screen.blit(casa, (1015, 420))
    screen.blit(casa, (1015, 520))
    screen.blit(casa, (1110, 420))
    screen.blit(casa, (1110, 520))

    # bloco 7
    screen.blit(casa, (220, 800))
    screen.blit(arvore, (110, 800))
    screen.blit(arvore, (170, 780))
    screen.blit(arvore, (130, 750))

    # bloco 8
    screen.blit(ap_pequeno, (710, 750))
    screen.blit(arvore, (610, 715))
    screen.blit(arvore, (610, 765))
    screen.blit(arvore, (610, 815))
    screen.blit(arvore, (510, 715))
    screen.blit(arvore, (510, 765))
    screen.blit(arvore, (510, 815))

    # bloco 9
    screen.blit(ap_pequeno, (1010, 800))
    screen.blit(arvore, (925, 720))
    screen.blit(arvore, (985, 720))
    screen.blit(arvore, (1045, 720))
    screen.blit(arvore, (1105, 720))

    font = pygame.font.SysFont("arial", 25)
    label_ep = font.render("Episodios", 1, (255,255,255))
    label_num_ep = font.render(str(episode), 1, (255,255,255))

    label_loss = font.render("Loss", 1, (255,255,255))
    label_num_loss = font.render(str(float("{:.4f}".format(loss))), 1, (255,255,255))

    screen.blit(label_ep, (1380, 100))
    screen.blit(label_num_ep, (1425, 130))

    screen.blit(label_loss, (1405, 250))
    screen.blit(label_num_loss, (1400, 280))

    pygame.display.flip()

def deepQLearning(model, ambiente):
    root = tkinter.Tk()
    root.withdraw()
    if os.path.isfile("model.h5"):
        result = messagebox.askquestion("Load", "Existe um modelo salvo, deseja carregar?", icon='info', type='yesno')
        if result == 'yes':
            model.load("model.h5")
            print("modelo carregado...")

    loss = [0]
    map_x = [-1, 10]
    map_y = [-1, 13]

    
    for episode in range(50):
        ambiente.iniciarNovamente()
        encerra_epoca = False
        
        next_state = ambiente.mapa.reshape((1, -1))

        while not encerra_epoca:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = messagebox.askquestion("Sair", "Deseja salvar o modelo antes de sair?", icon='info', type='yesno')
                    if result == 'yes':
                        model.save("model.h5")
                        print("modelo salvo...")
                    return

            valid_actions = ambiente.validarAcao()
            if not valid_actions:
                encerra_epoca = True
                continue

            current_state = next_state

            x, y, _, acao = ambiente.estado_atual
            desenharAmbiente(x, y, ambiente, acao, episode, loss[-1])
            
            if np.random.rand() < model.epsilon:
                action = random.choice(valid_actions)
            else:
                action = model.predict(current_state)
            
            next_state, reward, game_status = ambiente.acao(action)

            encerra_epoca = False
            
            if game_status == 'perdido' or game_status == 'vitoria':
                encerra_epoca = True 
                x, y, _, acao = ambiente.estado_atual
                desenharAmbiente(x, y, ambiente, acao, episode, loss[-1])

            model.addMemory(current_state, action, reward, next_state, encerra_epoca)
            loss.append(model.replay())
            map_x.append(x)
            map_y.append(y)

    root.destroy()
    plt.plot(loss)
    plt.ylabel('loss')
    plt.show()

    plt.hist2d(map_x, map_y, bins=100, normed=False, cmap='plasma')

    cb = plt.colorbar()
    cb.set_label('Número de ações')

    plt.title('Mapa de calor')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()

    model.save("model.h5")

def incluirPorLinha(linha, colunas = []):
    for c in colunas:
        ambiente.setarColisao(linha, c)

def criarCenario(ambiente):
    ambiente.setarPontoInicial(1, 1)
    ambiente.setarAlvo(8, 7)

    incluirPorLinha(1, [2, 3, 5, 6, 7, 9, 10, 11])
    incluirPorLinha(2, [1, 2, 3, 5, 6, 7, 9, 10, 11])
    incluirPorLinha(4, [1, 2, 3, 5, 6, 7, 9, 10, 11])
    incluirPorLinha(5, [1, 2, 3, 5, 6, 7, 9, 10, 11])
    incluirPorLinha(7, [1, 2, 3, 5, 6, 7, 9, 10, 11])
    incluirPorLinha(8, [1, 2, 3, 5, 6, 9, 10, 11])

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((TAMANHO_CENARIO_Y*120,TAMANHO_CENARIO_X*100)) 

    model = Agente(TAMANHO_CENARIO_X, TAMANHO_CENARIO_Y)
    ambiente = Ambiente(TAMANHO_CENARIO_X, TAMANHO_CENARIO_Y)
    criarCenario(ambiente);
    deepQLearning(model, ambiente)
    
    pygame.quit()
