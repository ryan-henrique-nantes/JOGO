import pygame
from pygame.sprite import RenderUpdates
from configuracao import *
from utils import UiComponente

class Menu:
  def __init__(self):
    #pega a superfice de display
    self.display_surface = pygame.display.get_surface()
    self.todos_sprites = pygame.sprite.Group()
    self.setup()

  def setup(self):
    centro_X = ((LARGURA_TELA / 2) - (10 / 2))
    centro_Y = ((ALTURA_TELA / 2) - (10 / 2))  
    self.botao_iniciar = UiComponente((centro_X, centro_Y), "Iniciar", "Courier", 30, AZUL, BRANCO, EstadoJogo.NOVO_JOGO)
    self.botao_sair = UiComponente((centro_X, centro_Y - 100), "Sair", "Courier", 30, AZUL, BRANCO, EstadoJogo.SAIR)     

    self.botoes = RenderUpdates(self.botao_iniciar, self.botao_sair)

  def run(self):
    mouse_up = False
    while True:
      for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
          pygame.quit()
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:         
          mouse_up = True
      self.display_surface.fill(AZUL)

      for botao in self.botoes:
        acao_ui = botao.update(pygame.mouse.get_pos(), mouse_up)
        if acao_ui is not None:
          return acao_ui

      self.botoes.draw(self.display_surface, self.botoes)
      pygame.display.flip()
