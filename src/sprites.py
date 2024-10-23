import pygame
from configuracao import *

class Generic(pygame.sprite.Sprite):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_rect(topleft = pos)
    self.z = z

class Parede(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.hitbox = self.rect.copy()

class Bau(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main'], item = None):
    super().__init__(pos, surf, groups, z)
    self.aberto = False
    self.item = item
    self.interagivel = True
    self.hitbox = self.rect.copy()

  def interagir(self, jogador):
    self.aberto = True
    if self.item != None:
      jogador.items.append(self.item)
      self.item = None

  def update(self, *args):
    if self.aberto:
      self.interagivel = False
      self.image = pygame.image.load('./sprites/objeto/bau_aberto.png')
  
class Porta(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)

class Pecas(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.hitbox = self.rect.copy()
    self.interagivel = True

  def interagir(self, jogador):
    jogador.items.append(self)
    self.interagivel = False
    self.kill()

class Puzzle(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.hitbox = self.rect.copy()
    self.interagivel = True