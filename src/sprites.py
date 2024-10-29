import pygame
from configuracao import *

class Generic(pygame.sprite.Sprite):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_rect(topleft = pos)
    self.z = z

class Parede(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.hitbox = self.rect.copy()

class Bau(Generic):
  def __init__(self, pos, surf, groups, z = CAMADAS['main'], item = None):
    super().__init__(pos, surf, groups, z)
    self.aberto = False
    self.item = item
    self.interagivel = True
    self.hitbox = self.rect.copy()

  def interagir(self, jogador):
    self.aberto = True
    if self.item != None:
      jogador.adicionar_item(self.item)
      self.item = None

  def update(self, *args):
    if self.aberto:
      self.interagivel = False
      self.image = pygame.image.load('./sprites/objeto/bau_aberto.png')
  
class Porta(Generic):
  def __init__(self, pos, surf, groups, nivel, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.interagivel = True  # Porta não interagível inicialmente
    self.nivel_atual = nivel
    self.hitbox = self.rect.copy()

  def interagir(self, jogador):
    if self.nivel_atual.grade == None:
      return
    match self.nivel_atual.jogo.estado_jogo:
      case EstadoJogo.NIVEL1:
        self.nivel_atual.jogo.estado_jogo = EstadoJogo.NIVEL2
      case EstadoJogo.NIVEL2:
        self.nivel_atual.jogo.estado_jogo = EstadoJogo.NIVEL3
      case EstadoJogo.NIVEL3:
        self.nivel_atual.jogo.estado_jogo = EstadoJogo.SAIR

class Grade(Parede):
  def __init__(self, pos, surf, groups, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    

class Pecas(Generic):
  def __init__(self, pos, surf, groups, nome, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.hitbox = self.rect.copy()
    self.interagivel = True
    self.nome = nome

  def interagir(self, jogador):
    jogador.adicionar_item(self)
    self.interagivel = False
    self.kill()

class Puzzle(Generic):
  def __init__(self, pos, surf, groups, puzzle, grade, z = CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.hitbox = self.rect.copy()
    self.interagivel = True
    self.puzzle = puzzle
    self.grade = grade

  def interagir(self, jogador):
    if self.puzzle is not None:
      if self.puzzle(jogador).run():
        self.grade.kill()
  
  def grade(self, grade):
    if self.puzzle is not None:
      self.grade = grade

class EncPeca(Generic):
  def __init__(self, pos, surf, groups, nome: str, z=CAMADAS['main']):
    super().__init__(pos, surf, groups, z)
    self.nome = nome
    self.hitbox = self.rect.copy()
    self.posicao_correta = False

class PecasMovel(Pecas):
  def __init__(self, pos, surf, groups, nome: str, encaixes: list[EncPeca], z=CAMADAS['main']):
    super().__init__(pos, surf, groups, nome, z)
    self.dragging = False
    self.offset = pygame.math.Vector2()
    self.encaixes = encaixes

  def update(self, *args):
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    if self.dragging:
      self.rect.center = pygame.math.Vector2(mouse_pos) + self.offset
      if not mouse_buttons[0]:  # Se o botão do mouse não estiver pressionado
        self.stop_drag()
    else:
      if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
        self.start_drag(mouse_pos)

  def start_drag(self, mouse_pos):
    self.dragging = True
    self.offset = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(mouse_pos)

  def stop_drag(self):
    self.dragging = False
    self.verificar_encaixe()

  def verificar_encaixe(self):
    for encaixe in self.encaixes:
      if self.rect.colliderect(encaixe.rect):
        self.rect.left = encaixe.rect.left
        if self.nome == encaixe.nome.replace('enc', ''):
          encaixe.posicao_correta = True