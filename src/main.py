# -*- coding: utf-8 -*-
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
    if self.estado_jogo == EstadoJogo.NIVEL1:
      self.mostrar_introducao()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      
      
      dt = self.clock.tick() / 1000
      match self.estado_jogo:
        case EstadoJogo.NIVEL1:
          self.nivel1.run(dt)
        case EstadoJogo.NIVEL2:
          self.nivel2.run(dt)
        case EstadoJogo.NIVEL3:
          self.nivel3.run(dt)
        case EstadoJogo.SAIR:
          pygame.quit()
          sys.exit()   
      pygame.display.update()
            
  def mostrar_introducao(self):
    introducao_texto = (
      "Você foi desafiado pelo seus amigos a se aventurar em um castelo abandonado, "
      "mas acabou preso. Seu objetivo é escapar desse castelo utilizando fluxogramas. "
      "A partir desta sala em diante contém desafios que você precisará desvendar para "
      "chegar a saída, envolvendo sequencial, condição e loop. Há peças espalhadas pela sala, "
      "você deve juntá-las para completar o painel em frente à porta."
    )
    continuar_texto = "Aperte 'Enter' para continuar"

    self.tela.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    y = 100

    for line in self.wrap_text(introducao_texto, font, LARGURA_TELA - 40):
      text_surface = font.render(line, True, (255, 255, 255))
      text_rect = text_surface.get_rect(center=(LARGURA_TELA // 2, y))
      self.tela.blit(text_surface, text_rect)
      y += 40

    continuar_surface = font.render(continuar_texto, True, (255, 255, 255))
    continuar_rect = continuar_surface.get_rect(center=(LARGURA_TELA // 2, y + 40))
    self.tela.blit(continuar_surface, continuar_rect)

    pygame.display.update()

    # Espera até que a tecla 'Enter' ou 'Return' seja pressionada
    esperando = True
    while esperando:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            esperando = False

    self.estado_jogo = EstadoJogo.NIVEL1

  def wrap_text(self, text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
      current_line.append(word)
      width, _ = font.size(' '.join(current_line))
      if width > max_width:
        current_line.pop()
        lines.append(' '.join(current_line))
        current_line = [word]

    if current_line:
      lines.append(' '.join(current_line))

    return lines

if __name__ == '__main__':
  jogo = Jogo()
  jogo.run()