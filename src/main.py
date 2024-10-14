import pygame, pygame.display, pygame.time, pygame.event, sys
from configuracao import *
from menu import Menu
from nivel_1 import Nivel_1

class Jogo:
  def __init__(self):
    pygame.init()
    self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Fluxo Escape')
    self.clock = pygame.time.Clock()
    self.menu = Menu(self.tela)
    self.estado_jogo = self.menu.run()
    if self.estado_jogo == EstadoJogo.SAIR:
      pygame.quit()
      sys.exit()
    else:
      self.nivel = Nivel_1()
      self.run()

  def run(self):
    while True:
      for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      dt = self.clock.tick() / 1000
      self.nivel.run(dt)
      pygame.display.update()

if __name__ == '__main__':
  jogo = Jogo()
  jogo.run()