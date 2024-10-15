import pygame
from configuracao import *
from jogador import Jogador
from player_movement import UiBarraPrincipal, UiInicioAcao, UiBotaoIniciar, UiAvancar

class Nivel_1:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.todos_sprites = pygame.sprite.Group()
    self.setup()
    
  def setup(self):
    self.jogador = Jogador((640, 360), self.todos_sprites)
    self.barra_principal = UiBarraPrincipal()
    self.inicio_acao = UiInicioAcao(self.barra_principal)
    self.botao_iniciar = UiBotaoIniciar(self.barra_principal)
    self.componentes = [self.inicio_acao, UiAvancar(self.barra_principal.x, self.barra_principal.y + self.barra_principal.altura + 20, self.inicio_acao.largura, self.barra_principal.altura - 2 * self.barra_principal.padding)]

  def handle_events(self, evento: pygame.event.Event):
    self.botao_iniciar.handle_input(evento)
    for componente in self.componentes:
      if isinstance(componente, UiAvancar):
        componente.handle_input(evento, self.componentes)
      else:
        componente.handle_input(evento)

  def run(self, dt):
    self.display_surface.fill('black')
    self.todos_sprites.draw(self.display_surface)
    self.barra_principal.draw(tela=self.display_surface)
    self.botao_iniciar.draw(tela=self.display_surface) 
    for componente in self.componentes:
      componente.draw(tela=self.display_surface)
    #self.jogador.handle_input()
    #self.jogador.update_position()
    self.todos_sprites.update()