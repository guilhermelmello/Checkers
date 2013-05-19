#-*- coding: utf-8 -*-

import copy

class Minimax(object):
	def __init__(self, depth, game):
		self.depth = depth
		self.game = game
	
	
	def start_minimax(self, board, player1, player2):
		p,m,r =  self.minimax(0, board, player1, player2, self.max_function, self.min_function)
		return p,m,r
	
	
	def minimax(self,depth, board, player1, player2, max_function, min_function):
		if depth >= self.depth or self.game.end_of_game():
			return None, None, self.static(player1,player2)
		else:
			moves = self.game.generate_moves(player1)
			my_move = None
			for p in moves:			# para cada peça com movimento
				for m in p[1]:		# para cada movimento da peça
					# gerar um novo estado
					b = copy.deepcopy(board)
					ns = self.new_state(b,p[0],m)
					
					# aplicar o minimax no novo estado analisando as jogadas do outro jogador
					n, move, value = self.minimax(depth+1, ns, player2, player1, min_function, max_function)
					print value
					
					if my_move == None or my_move[2] < value:
						my_move = p[0],m,value
			
			return my_move
	
	def new_state(self,board,piece,move):
		#print "gerar um novo estado para",piece.position,move
		r,c = piece.position
		board[r][c] = '.'
		board[move[0]][move[1]] = piece.group
		#for asd in board:
			#print asd
		return board
	
	
	def static(self,player1,player2):
		
		moves1 = self.game.generate_moves(player1)
		moves2 = self.game.generate_moves(player2)
		p1,p2 = 0,0
		
		for m in moves1:
			p1 += len(m[1])
		for m in moves2:
			p2 += len(m[1])
		
		return (p1/len(moves1)) - (p2/len(moves2))
	
	
	def max_function():
		pass
	
	
	def min_function():
		pass