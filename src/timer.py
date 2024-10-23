import pygame 

class Timer:
	def __init__(self,duracao,func = None):
		self.duracao = duracao
		self.funcao = func
		self.tempo_inicial = 0
		self.ativo = False

	def ativar(self):
		self.ativo = True
		self.tempo_inicial = pygame.time.get_ticks()

	def desativar(self):
		self.ativo = False
		self.tempo_inicial = 0

	def update(self):
		tempo_atual = pygame.time.get_ticks()
		if tempo_atual - self.tempo_inicial >= self.duracao:
			self.desativar()
			if self.funcao:
				self.funcao()