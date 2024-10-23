import pygame
from configuracao import *
from jogador import Jogador

class Overlay:
  def __init__(self, jogador: Jogador):
    self.display_surface = pygame.display.get_surface() 
    self.jogador = jogador
		
    overlay_path = './sprites/'
    if self.jogador.item_selecionado != None:
      self.items_surf = {item: pygame.image.load(f'{overlay_path}{item}.png').convert_alpha() for item in jogador.items}

  def display(self):
    if self.jogador.item_selecionado != None:
      item_surf = self.items_surf[self.jogador.item_selecionado]
      item_rect = item_surf.get_rect(midbottom = OVERLAY_POSITIONS['item'])
      self.display_surface.blit(item_surf,item_rect)