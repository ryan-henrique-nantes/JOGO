import pygame
from pygame.sprite import RenderUpdates
from configuracao import *
from utils import UiBotao, UiLabel

class Menu:
  def __init__(self, tela: pygame.Surface):
    #pega a superfice de display
    self.display_surface = pygame.display.get_surface()
    self.todos_sprites = pygame.sprite.Group()
    self.setup(tela.get_rect())

  def setup(self, rect: pygame.Rect): 
    self.titulo = UiLabel(rect, "Fluxo Escape", "Courier", 50, BRANCO, AZUL, 600)
    self.botao_iniciar = UiBotao(rect, "Iniciar", "Courier", 30, AZUL, BRANCO, 300, EstadoJogo.NIVEL1)
    self.botao_sair = UiBotao(rect, "Sair", "Courier", 30, AZUL, BRANCO, 250, EstadoJogo.SAIR)     

    self.botoes = RenderUpdates(self.titulo, self.botao_iniciar, self.botao_sair)

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
