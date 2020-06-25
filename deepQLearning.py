from collections import deque
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras import optimizers
import time
import random
import numpy as np

class Agente:
    def __init__(self, tamanho_x = 10, tamanho_y = 10, valores_saida = 4, epsilon = 1.0, gamma = 0.95):

        self.valores_saida = valores_saida
        self.tamanho_cenario = tamanho_x * tamanho_y
        self.memoria = deque(maxlen = 1000)
        
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon / 100
        self.epsilon_decay = epsilon - 0.005

        self.modelo = Sequential([
            Dense(64, input_shape=(self.tamanho_cenario,)),
            Activation("tanh"),
            Dense(32),
            Activation("tanh"),
            Dense(10),
            Activation("tanh"),
            Dense(self.valores_saida)
        ])
        
        self.modelo.compile(loss = 'mse', optimizer = 'adam')

    def addMemory(self, estado_atual, acao, recompensa, proximo_estato, fim_jogo):
        self.memoria.append((estado_atual, acao, recompensa, proximo_estato, fim_jogo))

    def replay(self, numero_treinos = 50):
        numero_treinos = min(len(self.memoria), numero_treinos)
        minimo_treino = random.sample(self.memoria, numero_treinos)

        entradas = np.zeros((numero_treinos, self.tamanho_cenario))
        alvos = np.zeros((numero_treinos, self.valores_saida))
        
        i = 0
        for estato, acao, recompensa, proximo_estato, concluido in minimo_treino:
            alvo = recompensa
            if not concluido:
                alvo = recompensa + self.gamma * np.amax(self.modelo.predict(proximo_estato)[0])
            alvo_focal = self.modelo.predict(estato)
            alvo_focal[0][acao] = alvo
            entradas[i] = estato
            alvos[i] = alvo_focal
            i += 1
        
        self.modelo.fit(entradas, alvos, epochs = 20, verbose = 0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return self.modelo.evaluate(entradas, alvos, verbose = 0)

    def predict(self, estado_atual):
        prever = self.modelo.predict(estado_atual)[0]
        ordenar = np.argsort(prever)[-len(prever):]
        ordenar = np.flipud(ordenar)
        return ordenar[0]

    def load(self, nome_arquivo):
        self.modelo.load_weights(nome_arquivo)

    def save(self, nome_arquivo):
        self.modelo.save_weights(nome_arquivo)