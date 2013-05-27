#-*- coding: utf-8 -*-

import copy,sys

class Minimax(object):
	def __init__(self, depth, game):
		self.depth = depth
		self.game = game
	
	#
	def start_minimax(self, board, player1, player2):
		p,m,v,c =  self.minimax(0, board, player1, player2, self.max_function, self.min_function)
		return p,m,v
	
	#
	def minimax(self,depth, board, player1, player2, max_function, min_function):
		if depth >= self.depth or self.game.end_of_game(board):											# se a profundidade foi alcaçada
			#print "\t"*depth,"FIM"
			return None, None, self.static(player1,player2,board), []											# aplicar a função estática
		else:
			moves = self.game.generate_moves(player1,board)
			
			
			#s = "\t"*depth
			#for bb in board:
				#print s,bb
			
			my_move = None
			
			#print s,player1[0].__class__
			#for psd in player1:
				#print s,psd.position,psd.get_moves(board)
			#print s,player2[0].__class__
			#for psd in player2:
				#print s,psd.position,psd.get_moves(board)
			
			for p in moves:			# para cada peça com movimento
				#print s,"==================+>",p[0].position,p[1],p[2]
				for m in p[1]:		# para cada movimento da peça
					
					#print s,p[0].position, m
					
					# gerar um novo estado
					b = copy.deepcopy(board)
					#print s,"id Tabuleiro",id(board),id(b)
					p1 = copy.deepcopy(player1)
					#print s,"id p1",id(player1),id(p1)
					p2 = copy.deepcopy(player2)
					#print s,"id p2",id(player2),id(p2)
					
					for pc in p1:	# para cada peça na cópia
						if pc.position == p[0].position:		#
							np = pc
					
					#np = copy.deepcopy(p[0])						# O ERRO ABAIXO DESCRITO DEVE SER REPARADO AQUI
					#np1 = copy.deepcopy(p1)
					#np2 = copy.deepcopy(p2)
					ns = self.new_state(b,np,m,p1,p2)
					"""# AQUI ESTÁ O ERRO, NO LUGAR DE P[0] DEVE ESTAR
																	# UMA CÓPIA DESTA PEÇA QUE ESTÁ NA CÓPIA DA LISTA
																	# EM QUE A PEÇA ORIGINAL ESTÁ (É TALVEZ NÃO FAÇA SENTIDO,
																	# MAS É ISSO E MESMO)
																	"""
					
					#for nnn in np2:
						#print s,">>>",nnn.position
					#print "sim, peça capturada", ns[3]
					
					#for bb in ns[0]:
						#print s,bb
					
					# aplicar o minimax no novo estado analisando as jogadas do outro jogador
					#n, move, value, cap = self.minimax(depth+1, nb, np2, np1, min_function, max_function)
					n, move, value, cap = self.minimax(depth+1, b, p2, p1, min_function, max_function)
					#print value
					
					if my_move == None or max_function(my_move[2],value) == value:
						#print "CAPTURA FINAL",copy.deepcopy(cap)
						#print "HERE",id(ns[3]),ns[3]
						my_move = p[0],m,value,copy.deepcopy(ns[3])
						#print "AQUI",id(ns[3]),ns[3]
			return my_move
	
	
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
	
	
	def static(self,player1,player2,board):
		if len(player1) == 0:
			return -1000
		elif len(player2) == 0:
			return 1000
		
		
		moves1 = self.game.generate_moves(player1,board)
		moves2 = self.game.generate_moves(player2,board)
		p1,p2 = 0,0
		
		for m in moves1:
			p1 += len(m[1])
		for m in moves2:
			p2 += len(m[1])
		
		return (p1/len(player1)) - (p2/len(player2))
	
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
	
	
	BOARD = [['#','.','#','.','#','b','#','.'],
			 ['.','#','.','#','b','#','.','#'],
			 ['#','b','#','b','#','.','#','r'],
			 ['.','#','.','#','.','#','b','#'],
			 ['#','r','#','.','#','.','#','b'],
			 ['.','#','.','#','r','#','r','#'],
			 ['#','r','#','.','#','r','#','r'],
			 ['.','#','.','#','.','#','.','#']]
	
	c = Checkers(screen)
	c.set_test(BOARD)
	
	print "RED"
	for p in c.red_pieces:
		print p.position,p.get_moves(BOARD)
	print "BLACK"
	for p in c.black_pieces:
		print p.position,p.get_moves(BOARD)
	
	m = Minimax(3,c)
	
	m.start_minimax(BOARD,c.black_pieces,c.red_pieces)
	
	
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
				  
	#test_board =   [['#','.','#','.','#','.','#','.'],
					#['.','#','.','#','b','#','b','#'],
					#['#','.','#','b','#','.','#','r'],
					#['b','#','.','#','.','#','b','#'],
					#['#','r','#','.','#','.','#','b'],
					#['.','#','.','#','r','#','r','#'],
					#['#','r','#','.','#','r','#','r'],
					#['.','#','.','#','.','#','.','#']]
	
	
	#reds = []
	#blacks = []
	#for row in range(len(test_board)):
		#for col in range(len(test_board[0])):
			#if test_board[row][col] == 'r':
				#p = RedPiece((row,col))
				#reds.append(p)
				
			#if test_board[row][col] == 'b':
				#p = BlackPiece((row,col))
				#blacks.append(p)
			
			#if test_board[row][col] == 'R':
				#p = RedPiece((row,col))
				#p.promote()
				#reds.append(p)
			#if test_board[row][col] == 'B':
				#p = BlackPiece((row,col))
				#p.promote()
				#blacks.append(p)
	
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

#(pretas) [(jogadas pretas)]
#(0, 5) [(1, 6)]
#(1, 4) [(2, 5)]
#(2, 1) [(3, 2), (3, 0)]
#(2, 3) [(3, 4), (3, 2)]
#(3, 6) [(4, 5)]




