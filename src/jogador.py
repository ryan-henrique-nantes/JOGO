import pygame
from configuracao import *

class Jogador(pygame.sprite.Sprite):
  def __init__(self, posicao, group):
    super().__init__(group)

    self.imagem = pygame.Surface((32,32))
    self.imagem.fill('green')
    self.rect = self.imagem.get_rect(center = posicao)
