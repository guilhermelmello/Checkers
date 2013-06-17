#-*- coding: utf-8 -*-

# NOTAS:
#	- Unir tudo em uma classe, de modo que a condição de cortes
#		seja passada como parâmetro entre as funções de maximização
#			e minimização.
#	- Alterar os parametros da função de utilidade para um estado (???)


import copy,sys

global INFINITY, CONTADOR_ESTADO

#----[ CLASS: Minimax ]-----------------------------------------------#
# Classe Minimax, responsável pelos métodos comuns às variações do
# algoritmo (com e sem cortes alfa-beta) como a geração de estados
# para criação da árvore de jogo e a função utilidade
class Minimax(object):
	global INFINITY, CONTADOR_ESTADO
	
	def __init__(self,profundidade, jogo, heuristica):
		global INFINITY, CONTADOR_ESTADO
		INFINITY = 1000
		CONTADOR_ESTADO = 0
		
		self.profundidade = profundidade
		self.heuristica = heuristica
		self.jogo = jogo
	
	# função responsável por calcular o valor de
	# uma configuração do tabuleiro para 'jogador'
	def utilidade(self,estado,jogador,oponente,heuristica="posicional"):
		j = None
		o = None
		
		if jogador[0].group == 'r' or jogador[0].group == 'R':
			j = estado.vermelhas
			o = estado.pretas
		elif jogador[0].group == 'b' or jogador[0].group == 'B':
			j = estado.pretas
			o = estado.vermelhas
		
		if len(j) == 0 or len(self.jogo.generate_moves(j,estado.tabuleiro)) == 0:
			return -INFINITY
		elif len(o) == 0 or len(self.jogo.generate_moves(o,estado.tabuleiro)) == 0:
			return INFINITY
		
		util1 = [[ 0, 4, 0, 4, 0, 4, 0, 4],
				 [ 4, 0, 3, 0, 3, 0, 3, 0],
				 [ 0, 3, 0, 2, 0, 2, 0, 4],
				 [ 4, 0, 2, 0, 1, 0, 3, 0],
				 [ 0, 3, 0, 1, 0, 2, 0, 4],
				 [ 4, 0, 2, 0, 2, 0, 3, 0],
				 [ 0, 3, 0, 3, 0, 3, 0, 4],
				 [ 4, 0, 4, 0, 4, 0, 4, 0]]
		
		util2 = [[ 0, 6, 0, 6, 0, 6, 0, 6],
				 [ 6, 0, 5, 0, 5, 0, 5, 0],
				 [ 0, 4, 0, 3, 0, 3, 0, 4],
				 [ 4, 0, 3, 0, 2, 0, 3, 0],
				 [ 0, 3, 0, 2, 0, 2, 0, 3],
				 [ 3, 0, 2, 0, 1, 0, 2, 0],
				 [ 0, 2, 0, 1, 0, 1, 0, 2],
				 [ 2, 0, 1, 0, 1, 0, 1, 0]]
		
		util3 = [[ 0, 7, 0, 7, 0, 7, 0, 7],
				 [ 6, 0, 5, 0, 5, 0, 5, 0],
				 [ 0, 4, 0, 3, 0, 3, 0, 4],
				 [ 4, 0, 3, 0, 2, 0, 3, 0],
				 [ 0, 3, 0, 2, 0, 2, 0, 3],
				 [ 3, 0, 2, 0, 1, 0, 2, 0],
				 [ 0, 2, 0, 1, 0, 1, 0, 2],
				 [ 2, 0, 1, 0, 1, 0, 1, 0]]
		
		if heuristica == "posicional":
			return self.utilidade_posicional(estado.tabuleiro,jogador,oponente,util1)
		elif heuristica == "avanco":
			return self.utilidade_posicional(estado.tabuleiro,jogador,oponente,util2)
		elif heuristica == "avanco2":
			return self.utilidade_posicional(estado.tabuleiro,jogador,oponente,util3)
		
	
	
	# faz o cálculo posicional considerando uma 'máscara' posicional
	# (util), que contém o peso de cada casa do tabuleiro
	def utilidade_posicional(self,tabuleiro,jogador,oponente,util):
		
		ponto_vermelhas = 0
		ponto_pretas = 0
		
		for i, lin in enumerate(tabuleiro):
			for j, casa in enumerate(lin):
				if casa == 'r':
					ponto_vermelhas += 2 * util[i][j]
				elif casa == 'R':
					ponto_vermelhas += 5 * util[i][j]
				elif casa == 'b':
					ponto_pretas += 2 * util[7-i][7-j]
				elif casa == 'B':
					ponto_pretas += 5 * util[7-i][7-j]
		
		if jogador[0].group == 'r' or jogador[0].group == 'R':
			return ponto_vermelhas - ponto_pretas
		else:
			return ponto_pretas - ponto_vermelhas
	
	
	# Verifica se o estado recebido é um estado
	# terminas, ou seja, deve ser aplicada a
	# função de avaliação neste estado
	def profundo_o_suficiente(self,estado,profundidade):
		return profundidade >= self.profundidade or self.jogo.fim_de_jogo(estado)
	
	
	# Recebe um estado e um movimento, retornando um novo estado.
	# O estado resultante é construído com a aplicação do movimento
	# no estado recebido.
	def proximo_estado(self, estado, movimento):
		novo_estado = copy.deepcopy(estado)
		novo_peca   = None
		jogador     = None
		oponente    = None
		
		# encontra o jogador responsável pelo lance
		pos_ini = movimento.pos_inicial
		casa = novo_estado.tabuleiro[pos_ini[0]][pos_ini[1]]
		if casa == 'r' or casa == 'R':
			jogador  = novo_estado.vermelhas
			oponente = novo_estado.pretas
		elif casa == 'b' or casa == 'B':
			jogador  = novo_estado.pretas
			oponente = novo_estado.vermelhas
		else:
			print "ERRO: proximo_estado - movimento inválido, casa vazia"
		
		# encontra a peça a ser movida
		for peca in jogador:
			if peca.position == movimento.pos_inicial:
				novo_peca = peca
				break
		
		# atualizar o estado
		self.proximo_estado_auxiliar(novo_peca,novo_estado,movimento)
		
		# remove as peças oponentes que foram capturadas
		for peca in copy.copy(oponente):
			pos = peca.position
			if pos in movimento.captura:
				novo_estado.tabuleiro[pos[0]][pos[1]] = '.'
				oponente.remove(peca)
		
		# promover a peça, após a jogada ela parou
		# em uma casa de coroação
		if novo_peca.position[0] == novo_peca.MAX_ROW:
			novo_peca.promote()
			pos_prom = novo_peca.position
			novo_estado.tabuleiro[pos_prom[0]][pos_prom[1]] = novo_peca.group
		
		return movimento,novo_estado
	
	
	# Faz a análise e geração do próximo estado, verificando
	# se existe captura ou não, tratando a captura em sequencia
	def proximo_estado_auxiliar(self,peca,estado, movimento):
		pos_ini = movimento.pos_inicial
		pos_fin = movimento.pos_final
		
		estado.tabuleiro[pos_ini[0]][pos_ini[1]] = '.'
		estado.tabuleiro[pos_fin[0]][pos_fin[1]] = peca.group
		peca.position = pos_fin
		pos_anterior = movimento.pos_inicial
		
		if len(movimento.captura) > 0:
			pos_cap = movimento.captura[-1]
			estado.tabuleiro[pos_cap[0]][pos_cap[1]] = 'x'
			
			cap_seq = peca.get_moves(estado.tabuleiro)
			if len(cap_seq[1]) > 0:
				movimento.pos_inicial = movimento.pos_final
				movimento.pos_meio.append(movimento.pos_final)
				movimento.pos_final = cap_seq[0][0]
				movimento.captura.append(cap_seq[1][0])
				
				self.proximo_estado_auxiliar(peca,estado,movimento)
				movimento.pos_inicial = pos_anterior
	
	
	#
	def sucessores(self, estado, jogador):
		"""
		Obs.: Tratar o caso da captura em sequencia após a primeira captura
		para casos em que há mais de uma possibilidade de caminhos.
		(BIFURCAÇÃO APÓS PRIMEIRA CAPTURA)
		"""
		if self.profundo_o_suficiente(estado,0):		# A profundidade não importa neste caso
			return [],[]								# apenas interessa saber os estados sucessores
														# caso exista algum
		else:
			proximos_estados = []						# lista com os próximos estados
			proximos_movimentos = []					# lista com os próximos movimentos
			movimentos = self.jogo.generate_moves(jogador,estado.tabuleiro)
			
			for peca in movimentos:						# para cada peça com movimento
				for i, jogada in enumerate(peca[1]):	# para cada jogada da peça
					if len(peca[2]) == len(peca[1]):
						movimento = Movimento(peca[0].position,[],jogada,[peca[2][i]])
					else:
						movimento = Movimento(peca[0].position,[],jogada,[])
					
					movimento,novo_estado = self.proximo_estado(estado,movimento)
					
					proximos_estados.append(novo_estado)
					proximos_movimentos.append(movimento)
			
			return proximos_estados,proximos_movimentos


#----[ CLASS: Decisao_Minimax ]---------------------------------------#
class Decisao_Minimax(Minimax):
	global INFINITY, CONTADOR_ESTADO
	
	def __init__(self,profundidade, jogo, heuristica):
		super(Decisao_Minimax,self).__init__(profundidade,jogo,heuristica)
	
	#
	def comecar(self,estado,jogador, oponente):
		#print "=======>> MINIMAX <<======="
		j,v = self.valor_max(estado,0,jogador, oponente)
		return j,v
	
	def comecar_teste(self,estado,jogador, oponente):
		global CONTADOR_ESTADO
		#print "=======>> MINIMAX: TESTE <<======="
		CONTADOR_ESTADO = 0
		#t_inicial = 
		self.valor_max(estado,0,jogador, oponente)
		return CONTADOR_ESTADO#, t_final-t_inicial
	
	
	#
	def valor_max(self,estado, profundidade, jogador, oponente):
		global CONTADOR_ESTADO
		CONTADOR_ESTADO += 1
		
		#print "Nível MAX"
		#ax = "\t"*profundidade
		#print ax,"Vermelhas:"
		#for x in estado.vermelhas:
			#print ax,x.position
		#print ax,"Pretas"
		#for x in estado.pretas:
			#print ax,x.position
		#print ax,"Tabuleiro" 
		#for l in estado.tabuleiro:
			#print ax,l
		
		if self.profundo_o_suficiente(estado,profundidade):
			x =  self.utilidade(estado, jogador, oponente, heuristica=self.heuristica)
			#print ax,"-->",x
			return None,x#self.utilidade(estado, jogador, oponente,heuristica=self.heuristica)
		
		melhor_valor  = -INFINITY
		melhor_jogada = None
		
		if jogador[0].__class__ == estado.vermelhas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.vermelhas)
		elif jogador[0].__class__ == estado.pretas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.pretas)
		
		for s,a in zip(suc_estados,suc_movimentos):
			jogada,valor = self.valor_min(s,profundidade+1,jogador, oponente)
			if melhor_valor < valor or melhor_jogada == None:
				melhor_valor  = valor
				melhor_jogada = a
		
		return melhor_jogada,melhor_valor
	
	
	#
	def valor_min(self,estado, profundidade, jogador, oponente):
		global CONTADOR_ESTADO
		CONTADOR_ESTADO +=1
		
		#print "Nível MIN"
		#ax = "\t"*profundidade
		#print ax,"Vermelhas:"
		#for x in estado.vermelhas:
			#print ax,x.position
		#print ax,"Pretas"
		#for x in estado.pretas:
			#print ax,x.position
		#print ax,"Tabuleiro" 
		#for l in estado.tabuleiro:
			#print ax,l
		
		if self.profundo_o_suficiente(estado,profundidade):
			x =  self.utilidade(estado, jogador, oponente, heuristica=self.heuristica)
			#print ax,"-->",x
			return None,x # self.utilidade(estado, jogador, oponente, heuristica=self.heuristica)
		
		melhor_valor  = INFINITY
		melhor_jogada = None
		
		if oponente[0].__class__ == estado.vermelhas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.vermelhas)
		elif oponente[0].__class__ == estado.pretas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.pretas)
		
		for s,a in zip(suc_estados,suc_movimentos):
			jogada,valor = self.valor_max(s,profundidade+1,jogador, oponente)
			if melhor_valor > valor or melhor_jogada == None:
				melhor_valor = valor
				melhor_jogada = a
		
		return melhor_jogada,melhor_valor


#----[ CLASS: Decisao_Alfa_Beta ]-------------------------------------#
class Decisao_Alfa_Beta(Minimax):
	global INFINITY
	
	def __init__(self,profundidade, jogo, heuristica):
		super(Decisao_Alfa_Beta,self).__init__(profundidade,jogo,heuristica)
	
	
	#
	def comecar(self,estado,jogador, oponente):
		j,v = self.valor_max(estado,-INFINITY,INFINITY,0,jogador, oponente)
		return j,v
	
	def comecar_teste(self,estado,jogador, oponente):
		global CONTADOR_ESTADO
		CONTADOR_ESTADO = 0
		self.valor_max(estado,-INFINITY,INFINITY,0,jogador, oponente)
		return CONTADOR_ESTADO
	
	#
	def valor_max(self,estado,alfa,beta, profundidade, jogador, oponente):
		global CONTADOR_ESTADO
		CONTADOR_ESTADO += 1
		
		if self.profundo_o_suficiente(estado,profundidade):
			return None,self.utilidade(estado, jogador, oponente, heuristica=self.heuristica)
		
		melhor_valor  = -INFINITY
		melhor_jogada = None
		
		if jogador[0].__class__ == estado.vermelhas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.vermelhas)
		elif jogador[0].__class__ == estado.pretas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.pretas)
		
		for s,a in zip(suc_estados,suc_movimentos):
			jogada,valor = self.valor_min(s,alfa,beta,profundidade+1,jogador, oponente)
			if melhor_valor < valor or melhor_jogada == None:
				melhor_valor  = valor
				melhor_jogada = a
			if melhor_valor >= beta:
				return melhor_jogada,melhor_valor
			alfa = melhor_valor
		
		return melhor_jogada,melhor_valor
	
	
	#
	def valor_min(self,estado,alfa,beta, profundidade, jogador, oponente):
		global CONTADOR_ESTADO
		CONTADOR_ESTADO += 1
		if self.profundo_o_suficiente(estado,profundidade):
			return None, self.utilidade(estado, jogador, oponente, heuristica=self.heuristica)
		
		melhor_valor  = INFINITY
		melhor_jogada = None
		
		if oponente[0].__class__ == estado.vermelhas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.vermelhas)
		elif oponente[0].__class__ == estado.pretas[0].__class__:
			suc_estados,suc_movimentos =  self.sucessores(estado, estado.pretas)
		
		for s,a in zip(suc_estados,suc_movimentos):
			jogada,valor = self.valor_max(s,alfa,beta,profundidade+1,jogador, oponente)
			if melhor_valor > valor or melhor_jogada == None:
				melhor_valor = valor
				melhor_jogada = a
			if melhor_valor <= alfa:
				return melhor_jogada,melhor_valor
			beta = melhor_valor
		
		return melhor_jogada,melhor_valor


#----[ CLASS: Estado ]------------------------------------------------#
class Estado(object):
	def __init__(self,vermelhas,pretas,tabuleiro):
		self.vermelhas = copy.deepcopy(vermelhas)
		self.pretas = copy.deepcopy(pretas)
		self.tabuleiro = copy.deepcopy(tabuleiro)


#----[ CLASS: Movimento ]---------------------------------------------#
class Movimento(object):
	def __init__(self,pos_inicial,pos_meio,pos_final,captura):
		self.pos_inicial = pos_inicial	# posição inicial da peça
		self.pos_meio    = pos_meio		# caminho percorrido durante a captura
		self.pos_final   = pos_final	# posição final da peça
		self.captura     = captura		# posição das peças capturadas


#----[ MAIN ]---------------------------------------------------------#
if __name__ == "__main__":
	from checkers import *
	import pygame
	
	pygame.init()
	
	screen = pygame.display.set_mode((0,0))
	
	c = Checkers(screen)
	
	test_board =   [['#','.','#','.','#','.','#','.'],
					['.','#','.','#','.','#','.','#'],
					['#','.','#','.','#','.','#','b'],
					['.','#','.','#','.','#','.','#'],
					['#','.','#','.','#','r','#','r'],
					['.','#','.','#','.','#','.','#'],
					['#','.','#','.','#','.','#','.'],
					['.','#','.','#','.','#','.','#']]
	
	#test_board =   [['#','.','#','.','#','.','#','.'],
					#['.','#','.','#','.','#','.','#'],
					#['#','.','#','.','#','b','#','.'],
					#['.','#','.','#','b','#','.','#'],
					#['#','.','#','.','#','.','#','.'],
					#['.','#','.','#','.','#','.','#'],
					#['#','.','#','.','#','.','#','.'],
					#['.','#','.','#','.','#','.','#']]
	
	#test_board =    [['#','b','#','b','#','b','#','b'],
					 #['b','#','b','#','b','#','b','#'],
					 #['#','b','#','b','#','b','#','b'],
					 #['.','#','.','#','.','#','.','#'],
					 #['#','.','#','.','#','.','#','.'],
					 #['r','#','r','#','r','#','r','#'],
					 #['#','r','#','r','#','r','#','r'],
					 #['r','#','r','#','r','#','r','#']]
	
	
	reds = []
	blacks = []
	for row in range(len(test_board)):
		for col in range(len(test_board[0])):
			if test_board[row][col] == 'r':
				p = RedPiece((row,col))
				reds.append(p)
				
			if test_board[row][col] == 'b':
				p = BlackPiece((row,col))
				blacks.append(p)
			
			if test_board[row][col] == 'R':
				p = RedPiece((row,col))
				p.promote()
				reds.append(p)
			if test_board[row][col] == 'B':
				p = BlackPiece((row,col))
				p.promote()
				blacks.append(p)
	
	
	#h = "avanco2"
	h = "posicional"
	dm = Decisao_Minimax(5,c,h)
	#dm = Decisao_Alfa_Beta(5,c,h)
	meu_estado = Estado(reds,blacks,test_board)
	
	print "Vermelhas"
	for p in meu_estado.vermelhas:
		print p.position
	print "Pretas"
	for p in meu_estado.pretas:
		print p.position
	for l in meu_estado.tabuleiro:
		print l
	
	#--------------
	#r = dm.utilidade(meu_estado,meu_estado.vermelhas,meu_estado.pretas,heuristica="avanco")
	#print r
	#--------------
	r = dm.comecar(meu_estado,meu_estado.vermelhas,meu_estado.pretas)
	
	print r[0].pos_inicial
	print r[0].pos_meio
	print r[0].pos_final
	print r[0].captura
	#--------------
	#h="posicional"
	#print dm.utilidade(meu_estado,meu_estado.vermelhas,meu_estado.pretas,heuristica=h)
	#print dm.utilidade(meu_estado,meu_estado.pretas,meu_estado.vermelhas,heuristica=h)
	
	#h="avanco"
	#print dm.utilidade(meu_estado,meu_estado.vermelhas,meu_estado.pretas,heuristica=h)
	#print dm.utilidade(meu_estado,meu_estado.pretas,meu_estado.vermelhas,heuristica=h)
	
	#h="avanco2"
	#print dm.utilidade(meu_estado,meu_estado.vermelhas,meu_estado.pretas,heuristica=h)
	#print dm.utilidade(meu_estado,meu_estado.pretas,meu_estado.vermelhas,heuristica=h)
	#--------------
	
#----[ END OF FILE ]--------------------------------------------------#
