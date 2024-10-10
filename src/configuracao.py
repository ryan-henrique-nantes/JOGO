#tela
import tkinter as tk
ALTURA_TELA = tk.Tk().winfo_screenheight() - 200
LARGURA_TELA = tk.Tk().winfo_screenwidth() - 200
TAMANHO = 64

# Estado do jogo
from enum import Enum
class EstadoJogo(Enum):
  """
    SAIR = 'saindo do jogo'
    TITULO = 'no titulo do jogo'
    NOVO_JOGO = 'iniciou jogo'
    PROXIMO_NIVEL = 'passou de fase'
    PAUSADO = 'pausou jogo'
    JOGANDO = 'jogo rodando'
    MONTANDO = 'montando comandos para personagem se mover'
    EXECUTANDO = 'executando comandos montados'
  """
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
  'parede': 2
}

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (106, 159, 181)