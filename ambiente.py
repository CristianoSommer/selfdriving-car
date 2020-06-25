import numpy as np

class Ambiente:
    def __init__(self, tamanho_x = 10, tamanho_y = 10):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        
        self.tamanho_cenario = self.tamanho_x * self.tamanho_y 
        
        self.mapa = np.ones((self.tamanho_x, self.tamanho_y))
        self.mapa_valores = np.zeros((self.tamanho_x, self.tamanho_y))

    def setarAlvo(self, x, y):
        self.alvo = (x, y)
        self.mapa[x, y] = 0.75
    
    def setarColisao(self, x, y):
        self.mapa[x, y] = 0.0

    def setarPontoInicial(self, x, y):
        self.inicio = (x, y)
        self.estado_atual = (x, y, 'iniciar', 0)
        self.mapa[x, y] = 0.5
    
    def iniciarNovamente(self):
        x, y = self.inicio

        self.setarPontoInicial(x, y)
        self.posicao_visitadas = set()

        self.recompensa_min = -0.5 * self.tamanho_cenario
        self.recompensa_total = 0
        self.mapa_valores = np.copy(self.mapa)
    
    def validarAcao(self):
        x, y, situacao, _ = self.estado_atual

        acoes = [0, 1, 2, 3]

        if x == 0:
            acoes.remove(1)
        elif x == self.tamanho_x - 1:
            acoes.remove(3)

        if y == 0:
            acoes.remove(0)
        elif y == self.tamanho_y - 1:
            acoes.remove(2)

        if x > 0 and self.mapa[x - 1, y] == 0.0:
            acoes.remove(1)
        if x < self.tamanho_x - 1 and self.mapa[x + 1, y] == 0.0:
            acoes.remove(3)

        if y > 0 and self.mapa[x, y - 1] == 0.0:
            acoes.remove(0)
        if y < self.tamanho_y - 1 and self.mapa[x, y + 1] == 0.0:
            acoes.remove(2)

        return acoes
    
    def atualizarEstadoAtual(self, acao):
        x, y, situacao, _ = self.estado_atual

        if self.mapa[x, y] > 0.0:
            self.posicao_visitadas.add((x, y))

        acoes_valida = self.validarAcao()

        if not acoes_valida:
            situacao = 'bloqueado'
        elif acao in acoes_valida:
            situacao = 'valido'
            self.mapa_valores[x, y] = 1.0
            if acao == 0:
                self.mapa_valores[x, y - 1] = 0.5
                y -= 1
            elif acao == 1:
                self.mapa_valores[x - 1, y] = 0.5
                x -= 1
            if acao == 2:
                self.mapa_valores[x, y + 1] = 0.5
                y += 1
            elif acao == 3:
                self.mapa_valores[x + 1, y] = 0.5
                x += 1
        else:
            situacao = 'invalido'

        self.estado_atual = (x, y, situacao, acao)
    
    def acao(self, acao):
        self.atualizarEstadoAtual(acao)
        
        recompensa = self.obterReconpensa()
        self.recompensa_total += recompensa

        status = self.statusJogo()
        
        return self.gradeEstado(), recompensa, status
    
    def gradeEstado(self):
        grade = np.ones((self.tamanho_x, self.tamanho_y))
        x, y, _, _ = self.estado_atual
        grade[x, y] = 0.5
        return grade.reshape((1, -1))

    def statusJogo(self):
        if self.recompensa_total < self.recompensa_min:
            return 'perdido'

        x, y, _, _ = self.estado_atual
        alvo_x, alvo_y = self.alvo
        if x == alvo_x and y == alvo_y:
            return 'vitoria'

        return 'valido'
    
    def obterReconpensa(self):
        x, y, situacao, _ = self.estado_atual
        alvo_x, alvo_y = self.alvo

        if x == alvo_x and y == alvo_y:
            return 1.0
        if situacao == 'bloqueado':
            return self.recompensa_min - 1
        if situacao == 'invalido':
            return -0.75
        if (x, y) in self.posicao_visitadas:
            return -0.25
        if situacao == 'valido':
            return -0.05