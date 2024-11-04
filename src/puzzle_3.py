import pygame
from configuracao import *
from camera import CameraGroup
from pytmx.util_pygame import load_pygame
from sprites import Generic, EncPeca, PecasMovel
from overlay import Overlay
from jogador import Jogador
import sys

class Puzzle_3:
  def __init__(self, jogador: Jogador):
    ajustar_resolucao()
    self.display_surface = pygame.display.get_surface()
    self.items = jogador.itens
    self.overlay = Overlay(jogador)
    self.todos_encaixes = []
    self.all_sprites = CameraGroup()
    self.bg_color = (0, 0, 0, 128)  # Semi-transparent black
    self.close_button_center = (35, 35)
    self.close_button_radius = 20
    self.close_button_color = (255, 0, 0)  # Red color for close button
    self.font = pygame.font.Font(None, 36)
    self.setup()
    self.running = True

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.close_button_rect.collidepoint(event.pos):
        self.running = False
        return True
    return False

  def setup(self):
    tmx_data = load_pygame('./data/puzzle nivel3.tmx')

    for camada in ['chão']:
      for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
        Generic((x * TAMANHO, y * TAMANHO), surf, self.all_sprites, CAMADAS['base_puzzle'])

    for camada in ['inicio1', 'fim1', 'linhas', 'vendanao', 'quantidade', 'vender1']:
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
    running = True
    while running:
      dt = pygame.time.Clock().tick(60) / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if self.is_close_button_clicked(event.pos):
            for encaixe in self.todos_encaixes:
              if not encaixe.posicao_correta:
                return False
            return True

      self.display_surface.fill(self.bg_color)
      self.all_sprites.update(dt)
      self.all_sprites.custom_draw(self.display_surface)
      self.overlay.display()

      # Desenhar o botão de fechar como um círculo vermelho com um 'X'
      pygame.draw.circle(self.display_surface, self.close_button_color, self.close_button_center, self.close_button_radius)
      self.draw_close_button_x()
      self.display_message("Este diagrama deve mostrar um processo onde o estoque de maçãs é verificado antes de cada venda. Se houver maçãs suficientes, a venda é concluída; caso contrário, a operação é interrompida. Essa estrutura deve ser baseada em uma condição que decide o próximo passo.")
      pygame.display.update()

  def is_close_button_clicked(self, mouse_pos):
    distance = pygame.math.Vector2(mouse_pos).distance_to(self.close_button_center)
    return distance <= self.close_button_radius

  def draw_close_button_x(self):
    x, y = self.close_button_center
    offset = self.close_button_radius // 2
    pygame.draw.line(self.display_surface, (255, 255, 255), (x - offset, y - offset), (x + offset, y + offset), 2)
    pygame.draw.line(self.display_surface, (255, 255, 255), (x + offset, y - offset), (x - offset, y + offset), 2)
  
  def display_message(self, message):
    words = message.split(' ')
    lines = []
    current_line = []
    max_width = LARGURA_TELA // 3  # Ajuste a largura máxima para 1/3 da tela
    space_width, _ = self.font.size(' ')

    for word in words:
      word_width, word_height = self.font.size(word)
      if sum(self.font.size(w)[0] for w in current_line) + space_width * len(current_line) + word_width <= max_width:
        current_line.append(word)
      else:
        lines.append(' '.join(current_line))
        current_line = [word]

    if current_line:
      lines.append(' '.join(current_line))

    y = 80  # Ajuste a posição inicial para mais para baixo
    line_spacing = 10  # Ajuste o espaçamento entre as linhas

    for line in lines:
      text_surface = self.font.render(line, True, (255, 255, 255))
      text_rect = text_surface.get_rect(topright=(LARGURA_TELA - 10, y))
      self.display_surface.blit(text_surface, text_rect)
      y += word_height + line_spacing