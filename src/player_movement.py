import pygame
from configuracao import *

def desenhar_componente(cor, tela: pygame.Surface, rect: pygame.Rect):
  pygame.draw.rect(tela, cor, rect)
      
  borda_esquerda = [
    (rect.left, rect.top),
    (rect.left - 8, rect.top),
    (rect.left - 8, rect.top + 5),
    (rect.left, rect.centery -5),
    (rect.left, rect.centery + 5),
    (rect.left - 8, rect.bottom - 5),
    (rect.left - 8, rect.bottom -1),
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

class IObserver:
  def update(self, x, y):
    pass

class ISubject:
  def __init__(self):
    self.filho = None

  def anexar(self, observer: IObserver):
    self.filho = observer

  def desanexar(self, observer: IObserver):
    if observer == self.filho:
      self.filho = None

  def notificar(self, x, y):
    if self.filho is not None:
      self.filho.update(x, y)

class UiBarraPrincipal:
  def __init__(self):
    self.largura_tela = LARGURA_TELA
    self.altura_tela = ALTURA_TELA
    self.largura = 600
    self.altura = 50
    self.x = (self.largura_tela - self.largura) // 2
    self.y = (self.altura_tela - (self.altura - 400)) // 2
    self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
    self.padding = 10   
    self.componentes = []

  def draw(self, tela: pygame.Surface):     
    pygame.draw.rect(tela, CINZA, self.rect, border_radius=25)

class UiInicioAcao(ISubject):
  def __init__(self, barraprincipal: UiBarraPrincipal):
    super().__init__()
    self.pai = barraprincipal
    self.padding = barraprincipal.padding
    self.largura = (self.pai.largura // 9)  - 2 * self.padding
    self.altura = self.pai.altura - 2 * self.pai.padding
    self.x = barraprincipal.x + self.padding 
    self.y = barraprincipal.y + self.padding 
    self.dragging = False
    self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
    self.offset_x = 0

  def draw(self, tela: pygame.Surface):
    pygame.draw.rect(tela, ROXO, self.rect, border_top_left_radius=25, border_bottom_left_radius=25)
    pontas_poligono= [
      (self.rect.right, self.rect.top + 6),
      (self.rect.right + 8, self.rect.centery - 5),
      (self.rect.right + 8, self.rect.centery + 5),
      (self.rect.right, self.rect.bottom - 6)
    ]
    pygame.draw.polygon(tela, ROXO, pontas_poligono)

  def handle_input(self, evento: pygame.event.Event):
    if evento.type == pygame.QUIT:
      pygame.quit()
    elif evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
      if self.rect.collidepoint(evento.pos):
        self.dragging = True
        mouse_x, _ = evento.pos
        self.offset_x = self.rect.x - mouse_x
        self.notificar(self.rect.x, self.rect.y)
    elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
      self.dragging = False
    elif evento.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
      if self.dragging:
        mouse_x, _ = evento.pos
        self.rect.x = mouse_x + self.offset_x
        self.rect.x = max(self.pai.x + self.padding, min(self.rect.x, self.pai.x + self.pai.largura - self.largura - self.padding))
        self.notificar(self.rect.x, self.rect.y)

class UiBotaoIniciar:
  def __init__(self, barraprincipal: UiBarraPrincipal):
    self.raio = 25
    self.pai = barraprincipal
    self.x = barraprincipal.x + barraprincipal.largura + self.raio + 10
    self.y = barraprincipal.y + barraprincipal.altura // 2
    self.cor = VERDE
    self.estado = EstadoBotao.PLAY

  def draw(self, tela: pygame.Surface):
    self.rect = pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)
    if self.estado == EstadoBotao.PLAY:
      pygame.draw.polygon(tela, BRANCO, [
        (self.x - 10, self.y - 15),
        (self.x - 10, self.y + 15),
        (self.x + 15, self.y)
      ])
    else:
      pygame.draw.rect(tela, BRANCO, (self.x - 10, self.y - 10, 20, 20))

  def handle_input(self, evento: pygame.event.Event):
    if evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
      if self.rect.collidepoint(evento.pos):
        self.alternar_botao()

  def alternar_botao(self):
    if self.estado == EstadoBotao.PLAY:
      self.estado = EstadoBotao.STOP
      self.cor = VERMELHO
    else:
      self.estado = EstadoBotao.PLAY
      self.cor = VERDE

class UiAvancar(ISubject, IObserver):
  def __init__(self, x, y, largura, altura):
    ISubject.__init__(self)
    IObserver.__init__(self)
    self.x = x
    self.y = y
    self.cor = VERDE_ESCURO
    self.largura = largura
    self.altura = altura
    self.rect = pygame.Rect(x, y, largura, altura)
    self.dragging = False
    self.posicao_original = (x, y)

  def draw(self, tela: pygame.Surface):
    desenhar_componente(self.cor, tela, self.rect)
    # Draw the arrow inside the rectangle
    arrow_points = [
      (self.rect.centerx - 10, self.rect.centery - 10),
      (self.rect.centerx - 10, self.rect.centery + 10),
      (self.rect.centerx + 10, self.rect.centery)
    ]
    pygame.draw.polygon(tela, BRANCO, arrow_points)

  def handle_input(self, evento, componentes):
    if evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
      if self.rect.collidepoint(evento.pos):
        self.dragging = True
        self.offset_x = self.rect.x - evento.pos[0]
        self.offset_y = self.rect.y - evento.pos[1]
        self.notificar(self.rect.x, self.rect.y)
    elif evento.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
      if self.dragging:
        self.dragging = False
        if not componentes[0].pai.rect.colliderect(self.rect):
          componentes.remove(self)
          self.desanexar(self.filho)
        novo_componente = UiAvancar(*self.posicao_original, self.largura, self.altura)
        componentes.append(novo_componente)
    elif evento.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
      if self.dragging:
        self.rect.x = evento.pos[0] + self.offset_x
        self.rect.y = evento.pos[1] + self.offset_y
        self.notificar(self.rect.x, self.rect.y)

  @property
  def acao(self):
    return 'avancar'