import pygame
from configuracao import *
from jogador import Jogador

class Overlay:
  def __init__(self, jogador: Jogador):
    self.display_surface = pygame.display.get_surface() 
    self.jogador = jogador

  def display(self):
    self.jogador.desenhar_itens(self.display_surface)