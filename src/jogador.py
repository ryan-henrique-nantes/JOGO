import pygame
from configuracao import *

class Jogador(pygame.sprite.Sprite):
    def __init__(self, posicao, group):
        super().__init__(group)
        
        self.image = pygame.Surface((32,32))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = posicao)
        