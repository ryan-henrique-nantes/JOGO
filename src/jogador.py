import pygame
from configuracao import *
from suporte import *
from timer import Timer
from sprites import Generic, Porta

class Jogador(pygame.sprite.Sprite):
  def __init__(self, posicao, group, collisao_sprites: list[Generic]):
    super().__init__(group)

    self.importar_assets()
    self.status = 'idle_down'
    self.frame_index = 0

    self.image = self.animacoes[self.status][self.frame_index]
    self.rect = self.image.get_rect(center = posicao)
    self.z = CAMADAS['main']

    # timers 
    self.timers = {
			'troca item': Timer(200),
    }

    self.direcao = pygame.math.Vector2()
    self.posicao = pygame.math.Vector2(self.rect.center)
    self.velocidade = 200

    self.collisao_sprites = collisao_sprites
    self.hitbox = self.rect.copy()

    self.items = {}
    self.itens = []
    self.item_selecionado = None
    self.objeto_interagivel_proximo = None

  def importar_assets(self):
    self.animacoes = {'idle_up': [],'idle_down': [],
                      'idle_left': [], 'idle_right': [], 
                      'walk_up':[], 'walk_down':[],
                      'walk_left':[], 'walk_right':[]}

    for animacao in self.animacoes.keys():
      caminho = './sprites/personagem/' + animacao
      self.animacoes[animacao] = import_folder(caminho)

  def animar(self,dt):
    self.frame_index += 4 * dt
    if self.frame_index >= len(self.animacoes[self.status]):
      self.frame_index = 0

    self.image = self.animacoes[self.status][int(self.frame_index)]

  def estado_jogo(self, estado_jogo):
    self.estado_jogo = estado_jogo

  def input(self):
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
      self.direcao.y = -1
      self.status = 'walk_up'
    elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
      self.direcao.y = 1
      self.status = 'walk_down'
    else:
      self.direcao.y = 0

    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
      self.direcao.x = 1
      self.status = 'walk_right'
    elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
      self.direcao.x = -1
      self.status = 'walk_left'
    else:
      self.direcao.x = 0

    if teclas[pygame.K_e] and self.objeto_interagivel_proximo:
      self.interagir()

  def interagir(self):
    if hasattr(self.objeto_interagivel_proximo, 'interagivel'):
      if self.objeto_interagivel_proximo.interagivel:
        self.objeto_interagivel_proximo.interagir(self)

  def adicionar_item(self, item):
    self.itens.append(item)
    nome_item = type(item).__name__
    if nome_item in self.items:
      self.items[nome_item] += 1
    else:
      self.items[nome_item] = 1

  def pegar_status(self):
    if self.direcao.magnitude() == 0:
      self.status = 'idle_' + self.status.split('_')[1]

  def atualizar_timers(self):
    for timer in self.timers.values():
      timer.update()

  def collision(self, direcao):
    for sprite in self.collisao_sprites:
      if hasattr(sprite, 'hitbox') and sprite.z == self.z:
        if sprite.hitbox.colliderect(self.hitbox):
          if direcao == 'horizontal':
            if self.direcao.x > 0:
              self.hitbox.right = sprite.hitbox.left
            if self.direcao.x < 0:
              self.hitbox.left = sprite.hitbox.right
            self.rect.centerx = self.hitbox.centerx
            self.posicao.x = self.hitbox.centerx

          if direcao == 'vertical':
            if self.direcao.y > 0:
              self.hitbox.bottom = sprite.hitbox.top
            if self.direcao.y < 0:
              self.hitbox.top = sprite.hitbox.bottom
            self.rect.centery = self.hitbox.centery
            self.posicao.y = self.hitbox.centery
        
  def mover(self,dt):
    if self.direcao.magnitude() > 0:  
      self.direcao = self.direcao.normalize()

    self.posicao.x += self.direcao.x * self.velocidade * dt
    self.hitbox.centerx = round(self.posicao.x)
    self.rect.centerx = self.hitbox.centerx
    self.collision('horizontal')

    self.posicao.y += self.direcao.y * self.velocidade * dt
    self.hitbox.centery = round(self.posicao.y)
    self.rect.centery = self.hitbox.centery
    self.collision('vertical')
    self.verificar_interacao()

  def get_target_pos(self):
    self.target_pos = self.rect.center + ALCANCE[self.status.split('_')[1]]

  def verificar_interacao(self):
    self.objeto_interagivel_proximo = None
    for sprite in self.collisao_sprites:
      if hasattr(sprite, 'hitbox') and hasattr(sprite, 'interagivel') and sprite.hitbox.collidepoint(self.target_pos):
        if sprite.interagivel:
          self.objeto_interagivel_proximo = sprite
          self.desenhar_mensagem_interacao(pygame.display.get_surface())

  def desenhar_mensagem_interacao(self, surface):
    if self.objeto_interagivel_proximo:
      font = pygame.font.Font(None, 36)
      text = font.render('E - Pegar/Interagir', True, (255, 255, 255))
      text_rect = text.get_rect(bottomright=(surface.get_width() - 10, surface.get_height() - 10))
      surface.blit(text, text_rect)

  def desenhar_itens(self, surface):
    font = pygame.font.Font(None, 36)
    x, y = surface.get_width() - 10, 10
    for item, quantidade in self.items.items():
      text = font.render(f'{item} x {quantidade}', True, (255, 255, 255))
      text_rect = text.get_rect(topright=(x, y + TAMANHO))
      surface.blit(text, text_rect)
      y += text_rect.height + 5

  def update(self, dt):
    self.input()
    self.pegar_status()
    self.atualizar_timers()
    self.get_target_pos()
    self.mover(dt)
    self.animar(dt)
    self.verificar_interacao()