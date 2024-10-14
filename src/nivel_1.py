import pygame
from configuracao import *
from jogador import Jogador

class Nivel_1:
  def __init__(self):

    #pega a superfice de display
    self.display_surface = pygame.display.get_surface()
    self.todos_sprites = pygame.sprite.Group()
    self.setup()
    
  def setup(self):
    self.jogador = Jogador((640, 360), self.todos_sprites)
    
 

  def run(self, dt):
    self.display_surface.fill('black')
    self.todos_sprites.draw(self.display_surface)
    self.jogador.handle_input()
    self.jogador.update_position()
    self.todos_sprites.update()