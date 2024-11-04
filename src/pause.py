import pygame
from configuracao import *
from pytmx.util_pygame import load_pygame
from sprites import Botao, Generic

class Pause:
  def __init__(self, jogo):
    self.jogo = jogo
    self.display_surface = pygame.display.get_surface()
    self.tmx_data = load_pygame('./data/pause.tmx')
    self.all_sprites = pygame.sprite.Group()
    self.setup()

  def setup(self):
    for camada in ['fundo', 'pause']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Generic((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, CAMADAS['main'])

    for camada in ['home']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Botao((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, self.jogo, EstadoJogo.TITULO, CAMADAS['main']) 

    for camada in ['resume']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Botao((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, self.jogo, self.jogo.estado_jogo_anterior, CAMADAS['main'])

    for camada in ['quit']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Botao((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, self.jogo, EstadoJogo.SAIR, CAMADAS['main'])

  def run(self, dt):
    mouse_up = False
    while True:
      for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
          pygame.quit()
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:         
          mouse_up = True
      self.display_surface.fill(AZUL)

      for botao in self.all_sprites:
        botao.click(pygame.mouse.get_pos(), mouse_up)

      self.all_sprites.draw(self.display_surface)
      pygame.display.flip()