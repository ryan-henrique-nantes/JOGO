import pygame, pygame.display, pygame.time, pygame.event, sys
from configuracao import *
from menu import Menu
from nivel_1 import Nivel_1
from nivel_2 import Nivel_2
from nivel_3 import Nivel_3

class Jogo:
  def __init__(self):
    pygame.init()
    self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Fluxo Escape')
    self.clock = pygame.time.Clock()
    self.menu = Menu(self.tela)
    self.estado_jogo = 0
    self.nivel1 = Nivel_1(self)
    self.nivel2 = Nivel_2(self)
    self.nivel3 = Nivel_3(self)

  def run(self):
    if self.estado_jogo == 0:
      self.estado_jogo = self.menu.run()
    if self.estado_jogo == EstadoJogo.SAIR:
      pygame.quit()
      sys.exit()
    self.estado_jogo = EstadoJogo.NIVEL3
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      
      dt = self.clock.tick() / 1000
      match self.estado_jogo:
      #  case EstadoJogo.NIVEL1:
      #    self.nivel1.run(dt)
      #  case EstadoJogo.NIVEL2:
      #    self.nivel2.run(dt)
        case EstadoJogo.NIVEL3:
          self.nivel3.run(dt)
        case EstadoJogo.SAIR:
          pygame.quit()
          sys.exit()   
      pygame.display.update()
            
if __name__ == '__main__':
  jogo = Jogo()
  jogo.run()