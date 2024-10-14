# tela
import tkinter as tk
ALTURA_TELA = tk.Tk().winfo_screenheight() - 200
LARGURA_TELA = tk.Tk().winfo_screenwidth() - 200
TAMANHO = 64

# Estado do jogo
from enum import Enum
class EstadoJogo(Enum):
    SAIR = -1
    TITULO = 0
    NOVO_JOGO = 1
    PROXIMO_NIVEL = 2
    PAUSADO = 3
    JOGANDO = 4
    MONTANDO = 5
    EXECUTANDO = 6

# Posicoes Camada
CAMADAS = {
    'vazio': 0,
    'chao': 1,
    'gui': 2
}

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (106, 159, 181)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
CINZA = (128, 128, 128)
ROXO = (128, 0, 128, 255)