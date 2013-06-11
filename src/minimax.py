#-*- coding: utf-8 -*-

import copy,sys

global INFINITY

class Minimax(object):
	def __init__(self, depth, game):
		self.depth = depth
		self.game = game
	
	#
	def start_minimax(self, board, player1, player2,reverse=False,heur="default"):
		p,m,v,c =  self.minimax(0, board, player1, player2, self.max_function, self.min_function,reverse=reverse,heur=heur)
		return p,m,v
	
	#
	def minimax(self,depth, board, player1, player2, max_function, min_function,reverse=False,heur="default"):
		if self.end_game(board):
			if len(player1) == 0:
				return  None,None,-1000, []
			else: return None,None,1000, []
		elif depth >= self.depth:											# se a profundidade foi alcaçada
			print "\t"*depth,"FIM",self.static(player1,player2,board,heur=heur)
			for l in board:
				print "\t"*depth,l
			return None, None, self.static(player1,player2,board,heur=heur), []		# aplicar a função estática
		else:
			
			moves = self.game.generate_moves(player1,board)
			
			
			s = "\t"*depth
			print "\n"
			for bb in board:
				print s,bb
			
			my_move = None
			
			print s,player1[0].__class__
			#for psd in player1:
				#print s,psd.position,psd.get_moves(board)
			#print s,player2[0].__class__
			#for psd in player2:
				#print s,psd.position,psd.get_moves(board)
			
			for p in moves:			# para cada peça com movimento
				#print s,"==================+>",p[0].position,p[1],p[2]
				for m in p[1]:		# para cada movimento da peça
					
					print s,p[0].position, m
					
					# gerar um novo estado
					b = copy.deepcopy(board)
					p1 = copy.deepcopy(player1)
					p2 = copy.deepcopy(player2)
					
					for pc in p1:	# para cada peça na cópia
						if pc.position == p[0].position:		#
							np = pc
					
					ns = self.new_state(b,np,m,p1,p2)
					if ns == None:
						if len(player1) == 0:
							return  None,None,-1000, []
						else: return None,None,1000, []
					
					
					n, move, value, cap = self.minimax(depth+1, b, p2, p1, min_function, max_function,heur=heur)
					if b == None:
						print ">>>>>>>>>> b"
					elif p2 == None:
						print ">>>>>>>>>> p2"
					elif p1 == None:
						print ">>>>>>>>>> p1"
					
					if reverse:
						if my_move == None or min_function(my_move[2],value) == value:
							my_move = p[0],m,value,copy.deepcopy(ns[3])
					elif my_move == None or max_function(my_move[2],value) == value:
						my_move = p[0],m,value,copy.deepcopy(ns[3])
			return my_move
	
	#
	def end_game(self,board):
		red = False
		black = False
		for row in board:
			for col in row:
				if col == 'r' or col == 'R':
					red = True
				elif col == 'b' or col == 'B':
					black = True
		if red and black:
			return False
		else: return True
	
	#
	def new_state(self,board,piece,move,p1,p2,captured=None):
	# encontrar a peça e verificar se o movimento realizado
	# possui capturas ou não, caso tenha capturas, gerar mais
	# um estado (após a captura), iniciando a recursão
	# caso contrário, não possui capturas, retornar o estado gerado
	# Obs.: ao realizar a captura, remover a peça adversária.
		if self.game.end_of_game(board):
			return
		#print "piece",piece.position,"id",id(piece)
		if captured == None:
			captured = []
		#print id(captured),captured
		my_move = [None,None] # movimento e captura
		piece_moves = piece.get_moves(board)
		for i,p_m in enumerate(piece_moves[0]):
			if p_m == move:
				my_move[0] = p_m
				break
			i += 1
		
		if i >= len(piece_moves[0]):
			print "ERRO <<<<<<<<<<<<============ "
			sys.exit()
		
		
		r,c = piece.position
		board[r][c] = '.'
		
		piece.position = move
		
		if piece.position[0] == piece.MAX_ROW:
			piece.promote()
		
		r,c = piece.position
		board[r][c] = piece.group
		
		if i < len(piece_moves[1]):
			#print "tem capturas"
			#print captured
			#print piece_moves[1][i]
			
			my_move[1] = piece_moves[1][i]
			board[my_move[1][0]][my_move[1][1]] = 'x'
			if captured.count(my_move[1]) == 0:
				#print "----",my_move[1]
				captured.append(my_move[1])
			other_moves = piece.get_moves(board)
			#print my_move
			#print "other_moves",other_moves
			if len(other_moves[1]) > 0:
				board,p1,p2,captured = self.new_state(board,piece,other_moves[0][0],p1,p2,captured=captured)
			else:
				#print "fim de capturas, remover peças capturadas"
				#print captured
				for c in copy.deepcopy(captured):
					board[c[0]][c[1]] = '.'
					for p in p2:
						if p.position == c:
							p2.remove(p)
							captured.remove(c)
							#print "removeu",p.position
				#captured = []
				
		#else:
			#print "sem capturas"
		
		
		
		#print "PECAS CAPTURADAS:",captured
		return board,p1,p2,captured
	
	
	
	# f1 = pesos dos tabuleiros
	# f2 = número de damas
	# f3 = captura e capuradas
	# f4 = 
	#
	def static(self,player1,player2,board,heur="default"):
		if player1[0].group == 'r' or player1[0].group == 'R':
			r = player1
			b = player2
		else:
			r = player2
			b = player1
		
		if heur == "checkers":		# Número de Damas
			print "Checkers Heuristic"
			return self.f2(r,b)
		elif heur == "captures":	# Número de capturas
			print "Captures Heuristic"
			return self.f3(r,b,board)
		elif heur == "mobility":	# Mobilidade das peças
			print "Mobility Heuristic"
			return self.f4(r,b,board)
		elif heur == "try":
			# OBS.: somar o número de damas à f1
			return self.f1(board) + self.f2(r,b)
			
		else:						# Força do tabuleiro
			#print "Board Power Heuristic"
			return self.f1(board)
		
	#
	def f1(self,board):
		"""
			Faz o cálculo da força do tabuleiro para as peças pretas
		"""
		red = 0
		black = 0
		for i, row in enumerate(board):
			for j, col in enumerate(board):
				if i in [3,4] and j in [3,4]:
					if board[i][j] == 'r':
						red += 2
					elif  board[i][j] == 'R':
						red += 5
					if board[i][j] == 'b':
						black += 2
					elif  board[i][j] == 'B':
						black += 5
				elif i in range(2,6) and j in range(2,6):
					if board[i][j] == 'r':
						red += 4
					elif  board[i][j] == 'R':
						red += 10
					if board[i][j] == 'b':
						black += 4
					elif  board[i][j] == 'B':
						black += 10
				elif i in range(1,7) and j in range(1,7):
					if board[i][j] == 'r':
						red += 6
					elif  board[i][j] == 'R':
						red += 15
					if board[i][j] == 'b':
						black += 6
					elif  board[i][j] == 'B':
						black += 15
				elif i in range(0,8) and j in range(0,8):
					if board[i][j] == 'r':
						red += 8
					elif  board[i][j] == 'R':
						red += 20
					if board[i][j] == 'b':
						black += 8
					elif  board[i][j] == 'B':
						black += 20
		return black-red
	#
	def f2(self,reds,blacks):
		"""
			Faz o cáculo de damas e peças que podem ser promovidas na próxima jogada
		"""
		r = 0
		b = 0
		for i in reds:
			if i.group == 'R':
				r += 5
			elif i.position[0] == i.MAX_ROW + 1:
				r += 3
		for i in blacks:
			if i .group == 'B':
				b += 5
			elif i.position[0] == i.MAX_ROW -1:
				b += 3
		return b-r
	#
	def f3(self,reds,blacks,board):
		"""
			calcula o número de capturas
		"""
		r = 0
		b = 0
		for p in reds:
			r += len( p.get_moves(board)[1] )
		
		for p in blacks:
			b += len( p.get_moves(board)[1] )
		
		return b-r
	#
	def f4(self,reds,blacks,board):
		"""
			cálculo da mobilidade
		"""
		r = 0
		b = 0
		for p in reds:
			r += len( p.get_moves(board)[0] )
		for p in blacks:
			b += len( p.get_moves(board)[0] )
		return b-r
	
	
	#
	def max_function(self,value1,value2):
		return max([value1,value2])
	
	#
	def min_function(self,value1,value2):
		return min([value1,value2])


#----[ MINIMAX TESTE ]------------------------------------------------#


class Decisao_Minimax(object):
	global INFINITY
	
	def __init__(self,profundidade, jogo):
		global INFINITY
		INFINITY = 1000
		
		self.profundidade = profundidade
		self.jogo = jogo
	
	
	#
	def comecar(self,estado,jogador, oponente):
		v = self.valor_max(estado,0,jogador, oponente)
		return v
	
	
	#
	def valor_max(self,estado, profundidade, jogador, oponente):
		print "MAX"
		
		if self.profundo_o_suficiente(estado,profundidade):
			return self.utilidade(estado.tabuleiro, jogador, oponente)
		
		v = -INFINITY
		
		
		for s in self.sucessores(estado, jogador):
			print "vermelhas"
			for k in s.vermelhas:
				print k.position
			print "pretas"
			for k in s.pretas:
				print k.position
			for k in s.tabuleiro:
				print k
			v = max(v, self.valor_min(s,profundidade+1,jogador, oponente))
		return v
	
	
	#
	def valor_min(self,estado, profundidade, jogador, oponente):
		print "MIN"
		
		if self.profundo_o_suficiente(estado,profundidade):
			return self.utilidade(estado.tabuleiro, jogador, oponente)
		v = INFINITY
		
		for s in self.sucessores(estado, oponente):
			v = min(v, self.valor_max(s,profundidade+1,jogador, oponente))
		return v
	
	#
	def utilidade(self,tabuleiro,jogador,oponente):
		global INFINITY
		
		if len(jogador) == 0 or len(self.jogo.generate_moves(jogador,tabuleiro)) == 0:
			return -INFINITY
		elif len(oponente) == 0 or len(self.jogo.generate_moves(oponente,tabuleiro)) == 0:
			return INFINITY
		
		red = 0
		black = 0
		for i, row in enumerate(tabuleiro):
			for j, col in enumerate(tabuleiro):
				casa = tabuleiro[i][j]
				if i in [3,4] and j in [3,4]:
					if casa == 'r':
						red += 2
					elif casa == 'R':
						red += 5
					if casa == 'b':
						black += 2
					elif  casa == 'B':
						black += 5
				elif i in range(2,6) and j in range(2,6):
					if casa == 'r':
						red += 4
					elif  casa == 'R':
						red += 10
					if casa == 'b':
						black += 4
					elif  casa == 'B':
						black += 10
				elif i in range(1,7) and j in range(1,7):
					if casa == 'r':
						red += 6
					elif  casa == 'R':
						red += 15
					if casa == 'b':
						black += 6
					elif  casa == 'B':
						black += 15
				elif i in range(0,8) and j in range(0,8):
					if casa == 'r':
						red += 8
					elif  casa == 'R':
						red += 20
					if casa == 'b':
						black += 8
					elif  casa == 'B':
						black += 20
		
		if jogador[0].group == 'r' or jogador[0].group == 'R':
			return red-black
		else:
			return black-red
	
	
	# OK
	def profundo_o_suficiente(self,estado,profundidade):
		return profundidade >= self.profundidade or self.jogo.fim_de_jogo(estado)
	
	
	# OK
	
	def proximo_estado(self, estado, movimento):
		"""
		Recebe um estado e um movimento, retornando um novo estado.
		O estado resultante é construído com a aplicação do movimento
		no estado recebido.
		"""
		novo_estado = copy.deepcopy(estado)
		novo_peca   = None
		jogador     = None
		oponente    = None
		
		pos_ini = movimento.pos_inicial
		casa = novo_estado.tabuleiro[pos_ini[0]][pos_ini[1]]
		if casa == 'r' or casa == 'R':
			jogador  = novo_estado.vermelhas
			oponente = novo_estado.pretas
		elif casa == 'b' or casa == 'B':
			jogador  = novo_estado.pretas
			oponente = novo_estado.vermelhas
		
		for peca in jogador:
			if peca.position == movimento.pos_inicial:
				novo_peca = peca
				break
		
		# atualizar o estado
		self.proximo_estado_auxiliar(novo_peca,novo_estado,movimento)
		
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
	
	
	def proximo_estado_auxiliar(self,peca,estado, movimento):
		"""
		Faz a análise e geração do próximo estado, verificando
		se existe captura ou não e tratando a captura em
		sequencia
		"""
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
				movimento.pos_final = cap_seq[0][0]
				movimento.captura.append(cap_seq[1][0])
				
				self.proximo_estado_auxiliar(peca,estado,movimento)
				movimento.pos_inicial = pos_anterior
	
	
	#
	def sucessores(self, estado, jogador):
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
						movimento = Movimento(peca[0].position,jogada,[peca[2][i]])
					else:
						movimento = Movimento(peca[0].position,jogada,[])
					movimento,novo_estado = self.proximo_estado(estado,movimento)
					proximos_estados.append(novo_estado)
					proximos_movimentos.append(movimento)
			
			return proximos_estados,proximos_movimentos
	
	


class Estado(object):
	
	# OBS.: Talvez seja necessário adicionar uma
	# lista para armazenar qual foi a jogada que
	# gerou o estado (armazenar o movimento)
	
	def __init__(self,vermelhas,pretas,tabuleiro):
		self.vermelhas = copy.deepcopy(vermelhas)
		self.pretas = copy.deepcopy(pretas)
		self.tabuleiro = copy.deepcopy(tabuleiro)


class Movimento(object):
	def __init__(self,pos_inicial,pos_final,captura):
		self.pos_inicial = pos_inicial
		self.pos_final   = pos_final
		self.captura     = captura



if __name__ == "__main__":
	from checkers import *
	import pygame
	
	pygame.init()
	
	screen = pygame.display.set_mode((0,0))
	
	c = Checkers(screen)
	
	#test_board =   [['#','.','#','.','#','.','#','.'],
					#['.','#','.','#','.','#','.','#'],
					#['#','.','#','.','#','.','#','.'],
					#['.','#','.','#','.','#','.','#'],
					#['#','.','#','.','#','.','#','.'],
					#['b','#','b','#','.','#','.','#'],
					#['#','r','#','r','#','.','#','.'],
					#['.','#','.','#','.','#','.','#']]
	
	test_board =   [['#','.','#','.','#','.','#','.'],
					['r','#','.','#','.','#','.','#'],
					['#','.','#','b','#','b','#','.'],
					['.','#','.','#','.','#','.','#'],
					['#','.','#','b','#','.','#','.'],
					['.','#','r','#','.','#','.','#'],
					['#','.','#','.','#','.','#','.'],
					['.','#','.','#','.','#','.','#']]
	
	
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
	
	
	dm = Decisao_Minimax(1,c)
	meu_estado = Estado(reds,blacks,test_board)
	
	
	print "Estado Recebido"
	print "Vermelhas"
	for p in meu_estado.vermelhas:
		print p.position
	print "Pretas"
	for p in meu_estado.pretas:
		print p.position
	print "Tabuleiro"
	for l in meu_estado.tabuleiro:
		print l
	
	es, mo = dm.sucessores(meu_estado,meu_estado.vermelhas)
	
	print "================"
	print "#  Sucessores  #"
	print "================"
	for e, m in zip(es,mo):
		print "Movimento"
		print "I:",m.pos_inicial
		print "F:",m.pos_final
		print "C:",m.captura
		print "Estado_Vermelhas"
		for k in e.vermelhas:
			print k.position
		print "Estado_pretas"
		for k in e.pretas:
			print k.position
		for l in e.tabuleiro:
			print l
	print "================"
	
	
	print "ONDE PAREI:"
	print "TESTAR O MÉTODO DE GERAÇÃO DE SUCESSORES PARA CASOS DE CAPTURA"
	
			
			
	
	
#----[ END OF FILE ]--------------------------------------------------#