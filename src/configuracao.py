# tela
import tkinter as tk
from pygame.math import Vector2

ALTURA_TELA = tk.Tk().winfo_screenheight() - 200
LARGURA_TELA = tk.Tk().winfo_screenwidth() - 200
TAMANHO = 32

def ajustar_resolucao():
  global ALTURA_TELA, LARGURA_TELA, TAMANHO

# Obtenha a resolução da tela do usuário
  root = tk.Tk()
  ALTURA_TELA = root.winfo_screenheight() - 200
  LARGURA_TELA = root.winfo_screenwidth() - 200
  root.destroy()

  # Ajuste o tamanho dos elementos do jogo conforme necessário
  TAMANHO = min(ALTURA_TELA, LARGURA_TELA) // 20  # Exemplo de ajuste do tamanho dos elementos

# Estado do jogo
from enum import Enum
class EstadoJogo(Enum):
    SAIR = -1
    TITULO = 0
    NIVEL1 = 1
    NIVEL2 = 2
    NIVEL3 = 3
    PAUSADO = 4
    FINAL = 5

class EstadoBotao(Enum):
    PLAY = 0
    STOP = 1

CAMADAS = {
	'void': 0,
	'ground': 1,
	'main': 2,
  'base_puzzle': 3,
  'puzzle': 4,
}

# overlay positions 
OVERLAY_POSITIONS = {
	'item' : (40, ALTURA_TELA - 15), 
}


ALCANCE = {
    'left': Vector2(-20, 0),
    'right': Vector2(20, 0),
    'up': Vector2(0, -20),
    'down': Vector2(0, 20)
}

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (106, 159, 181)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
CINZA = (128, 128, 128)
ROXO = (128, 0, 128, 255)
VERDE_ESCURO = (0, 150, 0)