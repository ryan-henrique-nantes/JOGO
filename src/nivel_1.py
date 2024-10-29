import pygame 
from configuracao import *
from jogador import Jogador
from overlay import Overlay
from sprites import Generic, Bau, Puzzle, Pecas, Porta, Parede, Grade
from camera import CameraGroup
from puzzle_1 import Puzzle_1
from pytmx.util_pygame import load_pygame

class Nivel_1:
  def __init__(self, jogo):
    self.display_surface = pygame.display.get_surface()
    self.all_sprites = CameraGroup()
    self.collisao_sprites = pygame.sprite.Group()
    self.porta = None
    self.jogo = jogo
    self.tmx_data = load_pygame('./data/nivel1.tmx') 
    self.setup()
    self.overlay = Overlay(self.jogador)

  def setup(self): 
    for camada in ['chão']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Generic((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, CAMADAS['ground'])

    for camada in ['parede', 'enfeites']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Parede((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    for camada in ['porta']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        self.porta = Porta((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], self, CAMADAS['main'])

    for camada in ['grade da porta']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        self.grade = Grade((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    for camada in ['puzzle']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Puzzle((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], Puzzle_1, self.grade, CAMADAS['ground'])

    for camada in ['peca AB1', 'peca AB2', 'peca C']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Pecas((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], camada, CAMADAS['ground'])

    for camada in ['bau']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Bau((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])
    self.jogador = Jogador((465, 555), self.all_sprites, self.collisao_sprites)
    
  def run(self, dt):
    self.display_surface.fill('black')
    self.all_sprites.custom_draw(self.jogador)
    self.all_sprites.update(dt)
    if self.grade is None:
      print('tste')
      return True
    self.overlay.display()