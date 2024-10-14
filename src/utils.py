import pygame, pygame.freetype, pygame.sprite
from pygame.freetype import SysFont
from enum import Enum

def criar_texto(texto: str, nome_fonte: str, tamanho_fonte: int, cor_texto: tuple[int, int, int], 
                cor_fundo: tuple[int, int, int]):
  """ 
  Cria uma superficie com texto, retornando-a, parametros:
    texto: texto a ser exibido,
    nome_fonte: fonte que deseja utilizar,
    tamanho_fonte: tamanho da fonte,
    cor_texto: cor do texto a ser exibido (tem que ser em rgb),
    cor_fundo: cor do fundo do texto (tem que ser em rgb)
  """
  fonte = SysFont(nome_fonte, tamanho_fonte, bold=True)
  superficie, _ = fonte.render(text=texto, fgcolor=cor_texto, bgcolor=cor_fundo)
  return superficie.convert_alpha()


class UiLabel(pygame.sprite.Sprite):
  """Um label de interface de usuário """

  def __init__(self, tamanho_tela: pygame.Rect, texto: str, nome_fonte:str, tamanho_fonte: int, 
                cor_texto: tuple[int, int, int], cor_fundo: tuple[int, int, int], padding: int = 0):
    """
    Parametros:
      posicao_central - tuple (x, y)
      texto: texto a ser exibido,
      nome_fonte: fonte que deseja utilizar,
      tamanho_fonte: tamanho da fonte,
      cor_texto: cor do texto a ser exibido (tem que ser em rgb),
      cor_fundo: cor do fundo do texto (tem que ser em rgb)
      padding - distancia de componente da borda da tela
    """
    imagem_padrao = criar_texto(texto, nome_fonte, tamanho_fonte, cor_texto, cor_fundo)
    self.tamanho_tela = tamanho_tela
    self.imagem = imagem_padrao
    self.padding = padding

    super().__init__()
  def calcular_posicao(self) -> pygame.Rect:
    return (self.tamanho_tela.width // 2, self.tamanho_tela.height - self.image.get_size()[1] - self.padding)
  
  @property
  def image(self):
    return self.imagem

  @property
  def rect(self):
    return self.image.get_rect(center=self.calcular_posicao())

  def draw(self, surface):
    """ Desenha componente na tela """
    surface.blit(self.image, self.rect) 

class UiBotao(pygame.sprite.Sprite):
  """Um elemento de interface de usuário """

  def __init__(self, tamanho_tela: pygame.Rect, texto: str, nome_fonte:str, tamanho_fonte: int, 
                cor_texto: tuple[int, int, int], cor_fundo: tuple[int, int, int], padding: int = 0, acao=None):
    """
    Parametros:
      posicao_central - tuple (x, y)
      texto: texto a ser exibido,
      nome_fonte: fonte que deseja utilizar,
      tamanho_fonte: tamanho da fonte,
      cor_texto: cor do texto a ser exibido (tem que ser em rgb),
      cor_fundo: cor do fundo do texto (tem que ser em rgb)
      padding - distancia de componente da borda da tela
      acao - o estado do jogo muda baseado nesse botao (ou não)
    """
    self.is_mouse_over = False
    self.tamanho_tela = tamanho_tela
    imagem_padrao = criar_texto(texto, nome_fonte, tamanho_fonte, cor_texto, cor_fundo)
    imagem_destacada = criar_texto(texto, nome_fonte, tamanho_fonte * 1.2, cor_texto, cor_fundo)
    self.padding = padding
    self.imagens = [imagem_padrao, imagem_destacada]

    self.rects = [
      imagem_padrao.get_rect(center=self.calcular_posicao()),
      imagem_destacada.get_rect(center=self.calcular_posicao()),
    ]

    self.acao = acao

    super().__init__()

  def calcular_posicao(self) -> pygame.Rect:
    return (self.tamanho_tela.width // 2, self.tamanho_tela.height - self.image.get_size()[1] // 2 - self.padding)

  @property
  def image(self):
    return self.imagens[1] if self.is_mouse_over else self.imagens[0]

  @property
  def rect(self):
    return self.rects[1] if self.is_mouse_over else self.rects[0]

  def update(self, posicao_mouse, mouse_sobre: bool):
    """ Verifica se mouse esta acima do texto e returna a ação do botão quando é apertado."""

    if self.rect.collidepoint(posicao_mouse):
      self.is_mouse_over = True
      if mouse_sobre:
        return self.acao
    else:
      self.is_mouse_over = False

  def draw(self, surface):
    """ Desenha componente na tela """
    surface.blit(self.image, self.rect)