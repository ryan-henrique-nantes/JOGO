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


class UiComponente(pygame.sprite.Sprite):
  """Um elemento de interface de usuário """

  def __init__(self, posicao_central, texto: str, nome_fonte:str, tamanho_fonte: int, 
                cor_texto: tuple[int, int, int], cor_fundo: tuple[int, int, int], acao=None):
    """
    Parametros:
      posicao_central - tuple (x, y)
      texto: texto a ser exibido,
      nome_fonte: fonte que deseja utilizar,
      tamanho_fonte: tamanho da fonte,
      cor_texto: cor do texto a ser exibido (tem que ser em rgb),
      cor_fundo: cor do fundo do texto (tem que ser em rgb)
      acao - o estado do jogo muda baseado nesse botao (ou não)
    """
    self.is_mouse_over = False

    imagem_padrao = criar_texto(texto, nome_fonte, tamanho_fonte, cor_texto, cor_fundo)
    imagem_destacada = criar_texto(texto, nome_fonte, tamanho_fonte * 1.2, cor_texto, cor_fundo)
    
    self.imagens = [imagem_padrao, imagem_destacada]
    print(posicao_central)
    self.rects = [
      imagem_padrao.get_rect(center=posicao_central),
      imagem_destacada.get_rect(center=posicao_central),
    ]

    self.acao = acao

    super().__init__()

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