import pygame
from configuracao import *
from camera import CameraGroup
from pytmx.util_pygame import load_pygame
from sprites import Generic, EncPeca, PecasMovel
from overlay import Overlay
from jogador import Jogador
import sys

class Puzzle_2:
  def __init__(self, jogador: Jogador):
    self.display_surface = pygame.display.get_surface()
    self.items = jogador.itens
    self.overlay = Overlay(jogador)
    self.all_sprites = CameraGroup()
    self.bg_color = (0, 0, 0, 128)  # Semi-transparent black
    self.close_button_rect = pygame.Rect(10, 10, 50, 30)
    self.close_button_color = (255, 0, 0)  # Red color for close button
    self.font = pygame.font.Font(None, 36)
    self.todos_encaixes = []
    self.setup()
    self.running = True

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.close_button_rect.collidepoint(event.pos):
        self.running = False
        return True
    return False

  def setup(self):
    tmx_data = load_pygame('./data/puzzle nivel2.tmx')

    for camada in ['chão']:
      for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
        Generic((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, CAMADAS['base_puzzle'])

    for camada in ['inicio1', 'fim1', 'linha1', 'chama', 'pergunta1']:
      for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
        Generic((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites], CAMADAS['puzzle'])

    for camada in ['encpeca A', 'encpeca B', 'encpeca C']:
      for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
        encaixes = EncPeca((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites], camada, CAMADAS['base_puzzle'])
        self.todos_encaixes.append(encaixes)

    for camada in self.items:
      if camada.nome in ['peca A', 'peca B', 'peca C']:
        for x, y, surf in tmx_data.get_layer_by_name(camada.nome).tiles():
          PecasMovel((x * TAMANHO, y * TAMANHO), surf, [self.all_sprites], camada.nome.replace('2', '1'), self.todos_encaixes, CAMADAS['puzzle'])

  def run(self):
    clock = pygame.time.Clock()
    while self.running:
      dt = clock.tick(60) / 1000  # Limitar a 60 FPS
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if self.handle_event(event):
          for encaixe in self.todos_encaixes:
            if not encaixe.posicao_correta:
              break
            return True


      self.display_surface.fill(self.bg_color)
      self.all_sprites.update(dt)
      self.all_sprites.custom_draw(self.display_surface)
      self.overlay.display()

      # Desenhar o botão de fechar
      pygame.draw.rect(self.display_surface, self.close_button_color, self.close_button_rect)
      close_button_text = self.font.render('X', True, (255, 255, 255))
      self.display_surface.blit(close_button_text, self.close_button_rect.topleft)

      pygame.display.update()