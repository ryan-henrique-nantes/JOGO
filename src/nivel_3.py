import pygame 
from configuracao import *
from jogador import Jogador
from overlay import Overlay
from sprites import Generic, Puzzle, Pecas, Porta, Parede, Grade
from camera import CameraGroup
from puzzle_3 import Puzzle_3
from pytmx.util_pygame import load_pygame

class Nivel_3:
  def __init__(self, jogo):
    ajustar_resolucao()
    self.display_surface = pygame.display.get_surface()
    self.all_sprites = CameraGroup()
    self.collisao_sprites = pygame.sprite.Group()
    self.porta = []
    self.grade = []
    self.jogo = jogo
    self.tmx_data = load_pygame('./data/nivel3.tmx') 
    self.setup()
    self.overlay = Overlay(self.jogador)

  def setup(self): 
    map_width = self.tmx_data.width * TAMANHO
    map_height = self.tmx_data.height * TAMANHO

    # Blocos de colisão na borda superior
    for x in range(0, map_width, TAMANHO):
      Parede((x, 0), pygame.Surface((TAMANHO, TAMANHO)), [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    # Blocos de colisão na borda inferior
    for x in range(0, map_width, TAMANHO):
      Parede((x, map_height - TAMANHO), pygame.Surface((TAMANHO, TAMANHO)), [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    # Blocos de colisão na borda esquerda
    for y in range(0, map_height, TAMANHO):
      Parede((0, y), pygame.Surface((TAMANHO, TAMANHO)), [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    # Blocos de colisão na borda direita
    for y in range(0, map_height, TAMANHO):
      Parede((map_width - TAMANHO, y), pygame.Surface((TAMANHO, TAMANHO)), [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    for camada in ['chão']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Generic((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, CAMADAS['ground'])

    for camada in ['parede', 'enfeite', 'porta_entrada']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Parede((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

    for camada in ['porta_saida']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        self.porta.append(Porta((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], self, CAMADAS['main']))

    for camada in ['grade']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        self.grade.append(Grade((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], self.porta, CAMADAS['main']))

    for camada in ['puzzle']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Puzzle((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], Puzzle_3, self.grade, CAMADAS['ground'])

    for camada in ['peca A', 'peca B', 'peca C']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        Pecas((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], camada, CAMADAS['ground'])

    for camada in ['spawn']:
      for x, y, surf in self.tmx_data.get_layer_by_name(camada).tiles():
        self.jogador = Jogador((x * TAMANHO, y * TAMANHO), self.all_sprites, self.collisao_sprites)
    
  def run(self, dt):
    self.display_surface.fill('black')
    self.all_sprites.custom_draw(self.jogador)
    self.all_sprites.update(dt)
    self.overlay.display()