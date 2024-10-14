import pygame
import sys
from configuracao import *
from jogador import Jogador

class UiAcoesPlayer:
  def __init__(self):
    pygame.init()
    self.largura_tela = LARGURA_TELA
    self.altura_tela = ALTURA_TELA
    self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
    pygame.display.set_caption("Bar Example")
    self.prompt_largura = 600
    self.prompt_altura = 50
    self.prompt_x = (self.largura_tela - self.prompt_largura) // 2
    self.prompt_y = (self.altura_tela - self.prompt_altura) // 2
    self.uiinicial_largura = self.prompt_largura // 9
    self.padding = 10
    self.uiinicial_x = self.prompt_x + self.padding
    self.uiinicial_y = self.prompt_y + self.padding
    self.dragging = False
    self.raio_botao = 25
    self.botao_x = self.prompt_x + self.prompt_largura + self.raio_botao + 10
    self.botao_y = self.prompt_y + self.prompt_altura // 2
    self.cor_botao = VERDE
    self.estado_botao = "play"
    self.acoes = []
    self.player_actions = []

  def draw(self):
    self.tela.fill(BRANCO)
    self.prompt_rect = pygame.Rect(self.prompt_x, self.prompt_y, self.prompt_largura, self.prompt_altura)
    pygame.draw.rect(self.tela, CINZA, self.prompt_rect, border_radius=25)
    self.uiinicial_rect = pygame.Rect(self.uiinicial_x, self.uiinicial_y, self.uiinicial_largura - 2 * self.padding, self.prompt_altura - 2 * self.padding)
    pygame.draw.rect(self.tela, ROXO, self.uiinicial_rect, border_top_left_radius=25, border_bottom_left_radius=25)
    pontas_poligono= [
      (self.uiinicial_rect.right, self.uiinicial_rect.top + 6),
      (self.uiinicial_rect.right + 8, self.uiinicial_rect.centery - 5),
      (self.uiinicial_rect.right + 8, self.uiinicial_rect.centery + 5),
      (self.uiinicial_rect.right, self.uiinicial_rect.bottom - 6)
    ]
    pygame.draw.polygon(self.tela, ROXO, pontas_poligono)

    # Draw the button
    pygame.draw.circle(self.tela, self.cor_botao, (self.botao_x, self.botao_y), self.raio_botao)
    if self.estado_botao == "play":
      pygame.draw.polygon(self.tela, BRANCO, [
        (self.botao_x - 10, self.botao_y - 15),
        (self.botao_x - 10, self.botao_y + 15),
        (self.botao_x + 15, self.botao_y)
      ])
    else:
      pygame.draw.rect(self.tela, BRANCO, (self.botao_x - 10, self.botao_y - 10, 20, 20))

    # Draw actions
    for acao in self.acoes:
      acao.draw(self.tela)

    pygame.display.flip()

  def handle_event(self, evento: pygame.event.Event):
    if evento.type == pygame.MOUSEBUTTONDOWN:
      if self.dragging:
        return  # Prevent selecting a new component while dragging
      if self.uiinicial_rect.collidepoint(evento.pos):
        self.dragging = True
        mouse_x, _ = evento.pos
        self.offset_x = self.uiinicial_rect.x - mouse_x
      elif (evento.pos[0] - self.botao_x) ** 2 + (evento.pos[1] - self.botao_y) ** 2 <= self.raio_botao ** 2:
        self.toggle_button()
      else:
        for acao in self.acoes:
          if acao.rect.collidepoint(evento.pos):
            acao.start_drag(evento.pos)
    elif evento.type == pygame.MOUSEBUTTONUP:
      self.dragging = False
      for acao in self.acoes:
        acao.stop_drag(evento.pos, self)
    elif evento.type == pygame.MOUSEMOTION:
      if self.dragging:
        mouse_x, _ = evento.pos
        self.uiinicial_x = mouse_x + self.offset_x
        self.uiinicial_x = max(self.prompt_x + self.padding, min(self.uiinicial_x, self.prompt_x + self.prompt_largura - self.uiinicial_largura - self.padding))
      for acao in self.acoes:
        acao.drag(evento.pos, self)

  def toggle_button(self):
    if self.estado_botao == "play":
      self.estado_botao = "stop"
      self.cor_botao = VERMELHO
    else:
      self.estado_botao = "play"
      self.cor_botao = VERDE

  def run(self):
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        self.handle_event(event)
      self.draw()
    pygame.quit()
    sys.exit()

class UiAvancar:
  def __init__(self, x: int, y: int, largura: int, altura: int):
    self.largura = largura
    self.altura = altura
    self.cor = (0, 150, 0)  # Dark green
    self.rect = pygame.Rect(x, y, self.largura, self.altura)
    self.dragging = False
    self.posicao_original = (x, y)

  def draw(self, tela: pygame.Surface):
    self.desenhar(self.cor, tela, self.rect)
    # Draw the arrow inside the rectangle
    arrow_points = [
      (self.rect.centerx - 10, self.rect.centery - 10),
      (self.rect.centerx - 10, self.rect.centery + 10),
      (self.rect.centerx + 10, self.rect.centery)
    ]
    pygame.draw.polygon(tela, BRANCO, arrow_points)

  def start_drag(self, posicao: tuple[int, int]):
    if self.rect.collidepoint(posicao):
      self.dragging = True
      self.offset_x = self.rect.x - posicao[0]
      self.offset_y = self.rect.y - posicao[1]

  def drag(self, posicao: tuple[int, int], ui: UiAcoesPlayer):
    if self.dragging:
        self.rect.x = posicao[0] + self.offset_x
        self.rect.y = posicao[1] + self.offset_y

        if self.rect.colliderect(ui.uiinicial_rect):
            # Calculate the position in the list
            x = max(ui.uiinicial_x + 55, min(self.rect.x, ui.uiinicial_x + ui.uiinicial_largura - self.largura))
            y = ui.uiinicial_y + len(ui.player_actions) * (self.rect.height + 10)  # Adjust y position based on list length

            self.rect.x = x
            self.rect.y = y

            if self not in ui.player_actions:
                ui.player_actions.append(self)
        else:
            if self in ui.player_actions:
                ui.player_actions.remove(self)

        # Handle reordering
        for i, action in enumerate(ui.player_actions):
            if action != self and self.rect.colliderect(action.rect):
                if self.rect.x < action.rect.x:
                    ui.player_actions.insert(i, self)
                else:
                    ui.player_actions.insert(i + 1, self)
                break

        # Reposition all actions in the list
        for i, action in enumerate(ui.player_actions):
            action.rect.x = ui.uiinicial_x + 55
            action.rect.y = ui.uiinicial_y + i * (action.rect.height + 10)


  def stop_drag(self, posicao: tuple[int, int], prompt: UiAcoesPlayer):
    if self.dragging:
      self.dragging = False
      if not ui.prompt_rect.colliderect(self.rect):
        if self in ui.player_actions:
          ui.player_actions.remove(self)
        ui.acoes.remove(self)
      nova_acao = UiAvancar(*self.posicao_original, self.largura, self.altura)
      ui.acoes.append(nova_acao)

  def desenhar(self, cor, tela: pygame.Surface, rect: pygame.Rect):
    pygame.draw.rect(tela, cor, rect)
        
    # Draw the left connector with a > shape
    borda_esquerda = [
      (rect.left, rect.top),
      (rect.left - 8, rect.top),
      (rect.left - 8, rect.top + 5),
      (rect.left, rect.centery -5),
      (rect.left, rect.centery + 5),
      (rect.left - 8, rect.bottom - 5),
      (self.rect.left - 8, rect.bottom -1),
      (rect.left, rect.bottom -1),
    ]
    pygame.draw.polygon(tela, cor, borda_esquerda)
          
    borda_direita= [
      (rect.right, rect.top + 6),
      (rect.right + 8, rect.centery - 5),
      (rect.right + 8, rect.centery + 5),
      (rect.right, rect.bottom - 6)
    ]
    pygame.draw.polygon(tela, cor, borda_direita)
        

  @property
  def acao(self):
    return 'avancar'

if __name__ == "__main__":
  ui = UiAcoesPlayer()
  # Place the UiAvancar component outside the purple bar
  ui.acoes.append(UiAvancar(ui.prompt_x, ui.prompt_y + ui.prompt_altura + 20, ui.uiinicial_largura - 2 * ui.padding, ui.prompt_altura - 2 * ui.padding))
  ui.run()