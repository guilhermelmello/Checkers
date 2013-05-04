#-*- coding: utf-8 -*-

"""
ONDE PAREI:
	- 1: ANALISAR E CONSERTAR O MÉTODO capture_pieces()
		Obs.: está retornando apenas uma possibilidade por peça - deve retornar uma lista com as possibilidades

"""


"""
CONFERÊNCIA

- método get_moves() está retornando os movimentos corretamente (testado para peças brancas)
"""

import sys, pygame, copy
import os
from abc import *
from math import *
from pygame.locals import *

global BOARD_MAP
global RED_DEFAULT,     RED_DEFAULT_SELECTED
global RED_CHECKER,     RED_CHECKER_SELECTED
global BLACK_DEFAULT, BLACK_DEFAULT_SELECTED
global BLACK_CHECKER, BLACK_CHECKER_SELECTED
global CAPTURE_MODE


def printBoardMap():
		for i in BOARD_MAP:
			print i


class Checkers(object):
	def __init__(self,file_name = "images/board1.png"):
		global BOARD_MAP
		global RED_DEFAULT,     RED_DEFAULT_SELECTED
		global RED_CHECKER,     RED_CHECKER_SELECTED
		global BLACK_DEFAULT, BLACK_DEFAULT_SELECTED
		global BLACK_CHECKER, BLACK_CHECKER_SELECTED
		global CAPTURE_MODE
		
		RED_DEFAULT				= pygame.image.load("images/red_default.png"           ).convert_alpha()
		RED_DEFAULT_SELECTED	= pygame.image.load("images/red_default_selected.png"  ).convert_alpha()
		RED_CHECKER				= pygame.image.load("images/red_checker.png"           ).convert_alpha()
		RED_CHECKER_SELECTED	= pygame.image.load("images/red_checker_selected.png"  ).convert_alpha()
		
		BLACK_DEFAULT 			= pygame.image.load("images/black_default.png"         ).convert_alpha()
		BLACK_DEFAULT_SELECTED	= pygame.image.load("images/black_default_selected.png").convert_alpha()
		BLACK_CHECKER			= pygame.image.load("images/black_checker.png"         ).convert_alpha()
		BLACK_CHECKER_SELECTED	= pygame.image.load("images/black_checker_selected.png").convert_alpha()
		
		CAPTURE_MODE = False
		
		
		#BOARD_MAP = [['#','b','#','b','#','b','#','b'],		# (r) - red piece
					 #['b','#','b','#','b','#','b','#'],		# (b) - black piece
					 #['#','b','#','b','#','b','#','b'],		# (#) - unplayable slot
					 #['.','#','.','#','.','#','.','#'],		# (.) - free slot
					 #['#','.','#','.','#','.','#','.'],		# (R) - red checker piece
					 #['r','#','r','#','r','#','r','#'],		# (B) - black checker piece
					 #['#','r','#','r','#','r','#','r'],
					 #['r','#','r','#','r','#','r','#']]
		
		#BOARD_MAP = [['#','.','#','.','#','.','#','.'],	# (r) - red piece
					 #['B','#','b','#','b','#','.','#'],	# (b) - black piece
					 #['#','.','#','.','#','.','#','.'],	# (#) - unplayable slot
					 #['R','#','b','#','b','#','b','#'],	# (.) - free slot
					 #['#','.','#','.','#','.','#','r'],	# (R) - red checker piece
					 #['.','#','b','#','.','#','.','#'],	# (B) - black checker piece
					 #['#','.','#','.','#','.','#','.'],
					 #['.','#','.','#','.','#','.','#']]
		
		#BOARD_MAP = [['#','.','#','.','#','.','#','.'],	# (r) - red piece
					 #['B','#','.','#','b','#','.','#'],	# (b) - black piece
					 #['#','.','#','.','#','.','#','.'],	# (#) - unplayable slot
					 #['R','#','.','#','b','#','b','#'],	# (.) - free slot
					 #['#','.','#','.','#','r','#','r'],	# (R) - red checker piece
					 #['.','#','.','#','.','#','.','#'],	# (B) - black checker piece
					 #['#','.','#','.','#','.','#','.'],
					 #['.','#','.','#','.','#','.','#']]
		
		BOARD_MAP = [['#','.','#','.','#','.','#','.'],	# (r) - red piece
					 ['.','#','.','#','.','#','.','#'],	# (b) - black piece
					 ['#','.','#','.','#','.','#','.'],	# (#) - unplayable slot
					 ['.','#','.','#','.','#','.','#'],	# (.) - free slot
					 ['#','b','#','.','#','b','#','r'],	# (R) - red checker piece
					 ['.','#','.','#','.','#','.','#'],	# (B) - black checker piece
					 ['#','.','#','b','#','b','#','.'],
					 ['.','#','.','#','r','#','.','#']]
		
		self.RED_TURN = True
		
		self.board_image = pygame.image.load(file_name).convert()
		self.red_pieces = []
		self.black_pieces = []
		self.selected_piece = None	# Set the selected piece
		
		self.TILE_X = self.board_image.get_size()[0]/8 		# number of pixels on x
		self.TILE_Y = self.board_image.get_size()[1]/8 		# number of pixels on y
		
		# Start the pieces on board
		for row in range(len(BOARD_MAP)):
			for col in range(len(BOARD_MAP[0])):
				if BOARD_MAP[row][col] == 'r':
					p = RedPiece((row,col))
					self.red_pieces.append(p)
					
				if BOARD_MAP[row][col] == 'b':
					p = BlackPiece((row,col))
					self.black_pieces.append(p)
				
				if BOARD_MAP[row][col] == 'R':										# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
					p = RedPiece((row,col))											# remover esta parte após conclusão
					p.promote()
					self.red_pieces.append(p)
				if BOARD_MAP[row][col] == 'B':
					p = BlackPiece((row,col))
					p.promote()
					self.black_pieces.append(p)										# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	
	
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(-1)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:	# left button
					if(self.RED_TURN):
						pieces = self.red_pieces		#  red  turn to select one piece
					else: pieces = self.black_pieces	# black turn to select one piece
					
					if not self.selected_piece and not CAPTURE_MODE:
						self.select_piece(pieces)
					else:
						self.move_piece(pieces)


	def select_piece(self,pieces):
		moves = self.generate_moves(pieces)
		piece = None
		
		#print "Moves"
		#for m in moves:
			#print m
		#print "====="
		
		for p in pieces:
			if p.rect.collidepoint(pygame.mouse.get_pos()):
				piece = p
		
		if piece:
			for m in moves:
				if piece.position == m[0].position:
					self.selected_piece = piece
					self.selected_piece.set_image_selected()
					break
			if not self.selected_piece:
				print "Peca Invalida"
		else: print "Selecione uma Peca"
		
		
		#print "+++++++++++++++++++"
				
	
	
	def move_piece(self,pieces):
		global CAPTURE_MODE
		x_m,y_m = pygame.mouse.get_pos()
		row = y_m/self.TILE_Y
		col = x_m/self.TILE_X
		
		# se a peça de selecionada for clicada, será deselecionada caso esteja em modo de captura
		if  self.selected_piece.rect.collidepoint(pygame.mouse.get_pos()) and not CAPTURE_MODE:
			self.selected_piece.set_image_default()
			self.selected_piece = None
		else:
			# senão irá tentar mover a peça para a nova posição
			print "===========> Move Piece"
			
			if CAPTURE_MODE:
				moves = self.generate_moves([self.selected_piece])
			else:
				moves = self.generate_moves(pieces)
			
			print "Movimentos"
			for m in moves:
				print m[0].position,m[1],m[2]
			
			move = []
			for m in moves:
				if m[0].position == self.selected_piece.position:
					move = m
			if move:
				print "-------> mover",self.selected_piece.position
				print move[0].position,move[1],move[2]
				
				x_p, y_p = self.selected_piece.position
				for i in range(len(move[1])):				# para cada movimento possivel
					print move[1][i]
					if (row,col) == move[1][i]:
						print "Jogada Válida"
						BOARD_MAP[x_p][y_p] = '.'
						BOARD_MAP[row][col] = self.selected_piece.group
						self.selected_piece.position = (row,col)
						if len(move[2]) > 0:				# a jogada posssui capturas
							CAPTURE_MODE = True
							print "--Remover",move[2][i]
							self.remove_piece(move[2][i])	# remover a peça capturada
							printBoardMap()
						else:								
							self.selected_piece.set_image_default()
							self.selected_piece = None
							self.RED_TURN = not self.RED_TURN
							CAPTURE_MODE = False
							return
						break
				
				
				print "<------- mover"
				print "p.position = ",self.selected_piece.position
				
				
				
			else:
				print "Jogada Inválida",self.selected_piece.position
			
			print "<=========== Move Piece"
			#i = 0
			#for i in range(len(moves)):
				#if(moves[i][0] == (row,col)):
					#break
				#i += 1
			## se existir o movimento - mover
			#if i < len(moves):
				## se tiver captura - iniciar CAPTURE_MODE
				#if len(moves[i][1]) > 0:
					#CAPTURE_MODE = True
					
			
			
			#for i in range(len(mov[1])):
				#x_p, y_p = self.selected_piece.position
				#if (row,col) == mov[1][i]:
					##print '->',mov[1][i],row,col
					#BOARD_MAP[x_p][y_p] = '.'
					#BOARD_MAP[row][col] = self.selected_piece.group
					##self.remove_piece(mov[2][i])
					#self.selected_piece.position = (row,col)
					
				#if len(mov[2]) == 0:
					#self.selected_piece.set_image_default()
					#self.selected_piece = None
					#self.RED_TURN = not self.RED_TURN
					#return
			
			#print "Jogada Invalida"
	
	
	
	def remove_piece(self, pos):
		if self.RED_TURN:
			pieces = self.black_pieces
		else: pieces = self.red_pieces
		for p in pieces:
			if p.position == pos:
				pieces.remove(p)
				BOARD_MAP[pos[0]][pos[1]] = '.'
				print "Peça removida",pos
				break
	
	def update(self,screen):
		for piece in self.red_pieces:
			x,y = piece.position
			piece.rect = screen.blit(piece.surface,(y*self.TILE_Y,x*self.TILE_X))
		
		for piece in self.black_pieces:
			x,y = piece.position
			piece.rect = screen.blit(piece.surface,(y*self.TILE_Y,x*self.TILE_X))
	
	
	def capture_pieces(self,board,piece):
		"""
			método invocado no modo de captura (CAPTURE_MODE)
			responsável por analisar as capturas em sequência
			possíveis e retornar o movimento (ou sequencia de
			jogadas) que tem maior número de capturas.
		"""
		moves = piece.get_moves(board)
		#print "cp:",moves
		
		
		if len(moves[1]) == 0:		# se não tiver capturas seguintes
			return 0,None,None		# retornar 0 para o número de capturas e None para a movimentação seguinte e a captura realizada
		
		count = 0
		next_move = []
		capt_move = []
		for i in range(len(moves[0])): 		# para cada movimento da peça - verificar o número de capturas realizadas
			#print "movimento:",moves[0][i]
			px,py = piece.position
			board[px][py] = '.'
			b = copy.deepcopy(board)
			p = copy.deepcopy(piece)
			p.position = moves[0][i]
			b[moves[0][i][0]][moves[0][i][1]] = p.group
			b[moves[1][i][0]][moves[1][i][1]] = 'x'
			
			c,nmov,cap = self.capture_pieces(b, p)
			c += 1
			if c > count:
				count = c
				next_move = [moves[0][i]]
				capt_move = [moves[1][i]]
				#print "Iniciado com",moves[0][i],moves[1][i]
			elif c == count:
				next_move.append(moves[0][i])
				capt_move.append(moves[1][i])
				#print "Inserido",moves[0][i],moves[1][i]
		
		return count, next_move, capt_move
		
	
	
	def generate_moves(self,pieces):
		"""
			método  responsável por analisar  e  retornar
			as jogadas possíveis de um conjunto de peças.
		"""
		"""
			OBS.: para jogadas com captura -> verificar o
			número capturas para cada jogada, e armazenar
			a jogada com maior número de capturas.
			- Iniciar CAPTURE_MODE
		"""
		moves = []
		captures = False
		for p in pieces:
			m = p.get_moves(BOARD_MAP)
			#print "==>>",p.position,m
			if len(m[0]) > 0: 		# SE TIVER JOGADAS
				if len(m[1]) > 0 and not captures: 	# se tiver capturas mas nenhuma captura adicionada
					moves = []						# limpar jogadas
					captures = True					# apenas jogadas com capturas
				if captures:									# se já tem capturas
					if len(m[1]) > 0:							# adicionar apenas jogadas com capturas
						moves.append([p, m[0],m[1]])
				else: moves.append([p, m[0],m[1]])		# se não tiver capturas, adicionar jogada
		
		#print "-> Moves:"
		#for kk in moves:
			#print kk[0].position,kk[1],kk[2]
		
		# até aqui moves representa as jogadas possíveis
		# caso existam jogadas com capturas, verificar
		# qual tem o maior número de capturas
		
		if captures:
			mc = [[None,[],[]]] # move/capture = [Piece,[(moves)],[(captures)]
			capt_num = 0
			
			
			for m in moves: # para cada peça com movimentos de captura
				#print "m:",m
				piece = m[0]
				
				#print "analise: ",m[0].position
				c,mov,cap = self.capture_pieces(copy.deepcopy(BOARD_MAP), copy.copy(piece))
				#print mov,c,cap
				
				if c > capt_num:
					capt_num = c
					mc = []
				if c == capt_num:
					mc.append([piece,mov,cap])
				
			#print "mc",mc
			
			return mc
		else:
			return moves


class Piece(object):
	global BOARD_MAP

	def __init__(self,surface,pos,group):
		self.surface = surface
		self.position = pos
		self.group = group
		self.rect = None
	
	def set_image_default(self):
		""" Define the image for a not selected piece """
		self.surface = self.default_image
	
	def set_image_selected(self):
		""" Define the image for a selected piece """
		self.surface = self.selected_image
	
	def is_next_move(self,row,col):
		moves,captures = self.generate_moves()
		for i in range(len(moves)):
			if (row,col) == moves[i]:
				return i
		return -1
	
	@abstractmethod
	def front_row(self,row):
		pass
	
	@abstractmethod
	def back_row(self,row):
		pass
	
	@abstractmethod
	def left_col(self, col):
		pass
	
	@abstractmethod
	def right_col(self, col):
		pass
	
	def is_move(self,row,col):
		if ( row < 8 and row >= 0 and col < 8 and col >= 0 ):
			return True
		else: return False
	
	def get_moves(self,board):
		moves = [[],[]]
		captures = False
		
		row,col = self.position
		
		#	 MOVEMENTO DE PEÇAS SIMPLES 	#
		if self.group == 'r' or self.group == 'b':
			new_row = self.front_row(row)
			new_col = self.left_col(col)
			if self.is_move(new_row,new_col):
				if board[new_row][new_col] == '.' and not captures:
					moves[0].append((new_row,new_col))
				elif board[new_row][new_col] in self.OPPONENT:
					new_row = self.front_row(new_row)
					new_col = self.left_col(new_col)
					if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
						if not captures:
							moves = [[],[]]
							captures = True
						moves[0].append((new_row,new_col))
						moves[1].append((self.back_row(new_row),self.right_col(new_col)))
			
			new_row = self.front_row(row)
			new_col = self.right_col(col)
			if self.is_move(new_row,new_col):
				if board[new_row][new_col] == '.' and not captures:
					moves[0].append((new_row,new_col))
				elif board[new_row][new_col] in self.OPPONENT:
					new_row = self.front_row(new_row)
					new_col = self.right_col(new_col)
					if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
						if not captures:
							moves = [[],[]]
							captures = True
						moves[0].append((new_row,new_col))
						moves[1].append((self.back_row(new_row),self.left_col(new_col)))
			
			new_row = self.back_row(row)
			new_col = self.left_col(col)
			if self.is_move(new_row,new_col) and board[new_row][new_col] in self.OPPONENT:
				new_row = self.back_row(new_row)
				new_col = self.left_col(new_col)
				if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
					if not captures:
						moves = [[],[]]
						captures = True
					moves[0].append((new_row,new_col))
					moves[1].append((self.front_row(new_row),self.right_col(new_col)))
			
			new_row = self.back_row(row)
			new_col = self.right_col(col)
			if self.is_move(new_row,new_col) and board[new_row][new_col] in self.OPPONENT:
				new_row = self.back_row(new_row)
				new_col = self.right_col(new_col)
				if self.is_move(new_row,new_col) and board[new_row][new_col] == '.':
					if not captures:
						moves = [[],[]]
						captures = True
					moves[0].append((new_row,new_col))
					moves[1].append((self.front_row(new_row),self.left_col(new_col)))
		
		#	 FIM MOVIMENTO DAS PEÇAS SIMPLES	#
		
		#	MOVIMENTO DE DAMAS	#
		elif self.group == 'R' or self.group == 'B':
			#	  DAMAS -> FRENTE / ESQUERDA 	# 
			new_row = self.front_row(row)
			new_col = self.left_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.front_row(new_row)
						c = self.left_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else:
							break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.front_row(new_row)
				new_col = self.left_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			#	  FIM DAMAS -> FRENTE / ESQUERDA 	# 
			
			#	  DAMAS -> FRENTE / DIREITA 	# 
			new_row = self.front_row(row)
			new_col = self.right_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.front_row(new_row)
						c = self.right_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else:
							break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.front_row(new_row)
				new_col = self.right_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			#	FIM DAMAS -> FRENTE / DIREITA	#
			
			#	  DAMAS -> ATRÁS / ESQUERDA 	# 
			new_row = self.back_row(row)
			new_col = self.left_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.back_row(new_row)
						c = self.left_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else:
							break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.back_row(new_row)
				new_col = self.left_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			
			#	FIM DAMAS -> ATRÁS / ESQUERDA	#
			
			#	  DAMAS -> ATRÁS / DIREITA 	# 
			new_row = self.back_row(row)
			new_col = self.right_col(col)
			m = [[],[]]	# possíveis movimentos gerados na diagonal
			eat = None	# armazena a peça capturada na diagonal
			while(self.is_move(new_row,new_col)):
				if board[new_row][new_col] in self.FRIEND:
					break
				elif board[new_row][new_col] in self.OPPONENT:
					if not eat:
						r = self.back_row(new_row)
						c = self.right_col(new_col)
						if self.is_move(r,c) and board[r][c] == ".":
							captures = True
							eat = (new_row,new_col)
							m = [[],[]]
						else:
							break
				elif board[new_row][new_col] == '.':
					m[0].append((new_row,new_col))
					if eat:
						m[1].append(eat)
				new_row = self.back_row(new_row)
				new_col = self.right_col(new_col)
			
			if len(m[1]) > 0:
				if len(moves[1]) == 0:
					moves = [[],[]]
				for i in m[0]:
					moves[0].append(i)
				for i in m[1]:
					moves[1].append(i)
			elif not captures:
				for i in m[0]:
					moves[0].append(i)
			
			#	FIM DAMAS -> ATRÁS / DIREITA	#
			
		#	 FIM MOVIMENTO DE DAMAS 	#
		return moves



class RedPiece(Piece):
	global RED_DEFAULT, RED_DEFAULT_SELECTED
	global RED_CHECKER, RED_CHECKER_SELECTED
	
	OPPONENT = ['b','B']
	FRIEND = ['r','R']
	MIN_COL = 0 # left
	MAX_COL = 7 # right
	MIN_ROW = 7 # back
	MAX_ROW = 0 # forward
	
	def __init__(self,pos):
		Piece.__init__(self,RED_DEFAULT,pos,'r')
		self.default_image  = RED_DEFAULT
		self.selected_image = RED_DEFAULT_SELECTED

	def promote(self):
		self.group = 'R'
		self.surface =        RED_CHECKER
		self.default_image  = RED_CHECKER
		self.selected_image = RED_CHECKER_SELECTED
	
	def front_row(self,row):
		return row - 1
	
	def back_row(self, row):
		return row + 1
	
	def left_col(self,col):
		return col - 1
	
	def right_col(self,col):
		return col + 1
	

class BlackPiece(Piece):
	global BLACK_DEFAULT, BLACK_DEFAULT_SELECTED
	global BLACK_CHECKER, BLACK_CHECKER_SELECTED
	
	OPPONENT = ['r','R']
	FRIEND = ['b','B']
	MIN_COL = 7 # left
	MAX_COL = 0 # right
	MIN_ROW = 0 # back
	MAX_ROW = 7 # forward
	
	def __init__(self,pos):
		Piece.__init__(self,BLACK_DEFAULT,pos,'b')
		self.default_image  = BLACK_DEFAULT
		self.selected_image = BLACK_DEFAULT_SELECTED

	def promote(self):
		self.group = 'B'
		self.surface =        BLACK_CHECKER
		self.default_image  = BLACK_CHECKER
		self.selected_image = BLACK_CHECKER_SELECTED
	
	def front_row(self,row):
		return row + 1
	
	def back_row(self, row):
		return row - 1
	
	def left_col(self,col):
		return col + 1
	
	def right_col(self,col):
		return col - 1


if __name__ == "__main__":
	pygame.init()
	pygame.display.set_caption("Checkers")
	
	os.environ['SDL_VIDEO_WINDOW_POS'] = '500,100'
	screen = pygame.display.set_mode((0,0))
	
	checkers = Checkers()
	screen = pygame.display.set_mode(checkers.board_image.get_size(),RESIZABLE,32)
	
	done = False
	while not done:
		
		pygame.display.flip()
		screen.fill((0,0,0))
		screen.blit(checkers.board_image,(0,0))
		
		checkers.update(screen)
		checkers.events()
	