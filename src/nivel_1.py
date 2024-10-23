import pygame 
from configuracao import *
from jogador import Jogador
from overlay import Overlay
from sprites import Generic, Bau, Puzzle, Pecas, Porta, Parede
from camera import CameraGroup
from pytmx.util_pygame import load_pygame

class Nivel_1:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collisao_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.jogador)

    def setup(self):
      tmx_data  = load_pygame('./data/nivel1.tmx')     

      for camada in ['chão']:
        for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
          Generic((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, CAMADAS['ground'])

      for camada in ['puzzle']:
        for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
          Puzzle((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['ground'])

      for camada in ['porta']:
        for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
          Porta((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

      for camada in ['parede', 'enfeites', 'grade da porta']:
        for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
          Parede((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])

      for camada in ['peça A', 'peça B', 'peça C']:
        for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
          Pecas((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['ground'])

      for camada in ['bau']:
        for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
          Bau((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites, self.collisao_sprites], CAMADAS['main'])
      self.jogador = Jogador((465, 555), self.all_sprites, self.collisao_sprites)


    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.jogador)
        self.all_sprites.update(dt)
        self.overlay.display()