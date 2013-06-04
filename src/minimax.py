#-*- coding: utf-8 -*-

import copy,sys

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

if __name__ == "__main__":
	from checkers import *
	import pygame
	
	pygame.init()
	
	screen = pygame.display.set_mode((0,0))
	
	
	#BOARD = [['#','.','#','.','#','b','#','.'],
			 #['.','#','.','#','b','#','.','#'],
			 #['#','b','#','b','#','.','#','r'],
			 #['.','#','.','#','.','#','b','#'],
			 #['#','r','#','.','#','.','#','b'],
			 #['.','#','.','#','r','#','r','#'],
			 #['#','r','#','.','#','r','#','r'],
			 #['.','#','.','#','.','#','.','#']]
	
	c = Checkers(screen)
	#c.set_test(BOARD)
	
	#print "RED"
	#for p in c.red_pieces:
		#print p.position,p.get_moves(BOARD)
	#print "BLACK"
	#for p in c.black_pieces:
		#print p.position,p.get_moves(BOARD)
	
	#m = Minimax(3,c)
	
	#m.start_minimax(BOARD,c.black_pieces,c.red_pieces)
	
	
	##---[ TESTANDO O GERADOR DE ESTADOS ]-------------------------------#
	
	##test_board = [['#','.','#','.','#','.','#','.'],
				  ##['.','#','.','#','b','#','.','#'],
				  ##['#','b','#','b','#','b','#','r'],
				  ##['r','#','.','#','.','#','b','#'],
				  ##['#','.','#','.','#','.','#','b'],
				  ##['.','#','.','#','r','#','r','#'],
				  ##['#','r','#','.','#','r','#','r'],
				  ##['.','#','.','#','.','#','.','#']]
	
	##test_board = [['#','.','#','.','#','b','#','.'],
				  ##['.','#','.','#','b','#','.','#'],
				  ##['#','b','#','b','#','.','#','r'],
				  ##['.','#','.','#','.','#','b','#'],
				  ##['#','r','#','.','#','.','#','b'],
				  ##['.','#','.','#','r','#','r','#'],
				  ##['#','r','#','.','#','r','#','r'],
				  ##['.','#','.','#','.','#','.','#']]
				  
	test_board =   [['#','B','#','.','#','.','#','.'],
					['.','#','.','#','b','#','b','#'],
					['#','.','#','b','#','.','#','r'],
					['b','#','.','#','.','#','b','#'],
					['#','r','#','.','#','.','#','b'],
					['.','#','.','#','r','#','r','#'],
					['#','r','#','.','#','r','#','r'],
					['.','#','.','#','.','#','.','#']]
	
	test_board =   [['#','B','#','.','#','R','#','.'],
					['.','#','.','#','r','#','.','#'],
					['#','.','#','b','#','.','#','r'],
					['b','#','.','#','.','#','b','#'],
					['#','r','#','.','#','.','#','b'],
					['.','#','.','#','r','#','r','#'],
					['#','b','#','b','#','r','#','r'],
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
	
	
	print ">",Minimax(None,c).f4(reds,blacks,test_board)
	
	#p1 = reds
	#p2 = blacks
	
	##print p1[0].__class__
	##for p in p1:
		##print p.position,p.get_moves(test_board)
	##print p2[0].__class__
	##for p in p2:
		##print p.position,p.get_moves(test_board)
	
	#m  = Minimax(2,c)
	
	#for p in p2:
		#if p.position == (3,0):
			#for mo in p.get_moves(test_board)[0]:
				
				
				#print "TESTANDO GERADOR DE ESTADOS PARA",p.position,mo
				##print "ANTES",p2[0].__class__
				##for l in p2:
					##print id(l),l.position
				
				##print "ANTES",p1[0].__class__
				##for l in p1:
					##print id(l),l.position
				
				
				#new_board = copy.deepcopy(test_board)
				#new_p = copy.deepcopy(p)
				#new_p1 = copy.deepcopy(p1)
				#new_p2 = copy.deepcopy(p2)
				#for np2 in new_p2:
					#if np2.position == p.position:
						#new_p = np2
				
				##print "\nNOVAS ANTES",new_p2[0].__class__
				##for l in new_p2:
					##print id(l),l.position
				
				##print "\nNOVAS ANTES",new_p1[0].__class__
				##for l in new_p1:
					##print id(l),l.position
				
				#print "TABULEIRO ANTES"
				#for l in test_board:
					#print l
				#print "NOVO TABULEIRO ANTES"
				#for l in new_board:
					#print l
				
				#new_board, new_p2, new_p1, cap = m.new_state(new_board,new_p,mo,new_p2,new_p1)# pretas jogam
				
				#print "TABULEIRO DEPOIS"
				#for l in test_board:
					#print l
				#print "NOVO TABULEIRO DEPOIS"
				#for l in new_board:
					#print l
				
				##print "\nDEPOIS",p2[0].__class__
				##for l in p2:
					##print id(l),l.position
				##print "\nDEPOIS",p1[0].__class__
				##for l in p1:
					##print id(l),l.position
				
				##print "\nNOVAS DEPOIS",new_p2[0].__class__
				##for l in new_p2:
					##print id(l),l.position
				##print "\nNOVAS DEPOIS",new_p1[0].__class__
				##for l in new_p1:
					##print id(l),l.position
			
			
	
	
#----[ END OF FILE ]--------------------------------------------------#