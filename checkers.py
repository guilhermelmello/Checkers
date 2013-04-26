import sys, pygame
from math import *
from pygame.locals import *

global BOARD_MAP

def printBoardMap():
		for i in BOARD_MAP:
			print i
		print "\n"


class Checkers(object):
	def __init__(self,file_name = "images/board1.png",red_first = True):
		global BOARD_MAP
		self.RED_DEFAULT			= pygame.image.load("images/red_default.png"         ).convert_alpha()
		self.RED_DEFAULT_SELECTED	= pygame.image.load("images/red_default_selected.png").convert_alpha()
		self.RED_CHECKER			= pygame.image.load("images/red_checker.png"         ).convert_alpha()
		self.RED_CHECKER_SELECTED	= pygame.image.load("images/red_checker_selected.png").convert_alpha()
		
		self.BLACK_DEFAULT 			= pygame.image.load("images/black_default.png"         ).convert_alpha()
		self.BLACK_DEFAULT_SELECTED	= pygame.image.load("images/black_default_selected.png").convert_alpha()
		self.BLACK_CHECKER			= pygame.image.load("images/black_checker.png"         ).convert_alpha()
		self.BLACK_CHECKER_SELECTED	= pygame.image.load("images/black_checker_selected.png").convert_alpha()
		
		self.RED_TURN = red_first
		
		BOARD_MAP = [['#','r','#','r','#','r','#','r'],	# (r) - red piece
					 ['r','#','r','#','r','#','r','#'],	# (b) - black piece
					 ['#','r','#','r','#','r','#','r'],	# (#) - unplayable slot
					 ['.','#','.','#','.','#','.','#'],	# (.) - free slot
					 ['#','.','#','.','#','.','#','.'],	# (R) - red checker piece
					 ['b','#','b','#','b','#','b','#'],	# (B) - black checker piece
					 ['#','b','#','b','#','b','#','b'],
					 ['b','#','b','#','b','#','b','#']]
		
		#BOARD_MAP = [['#','.','#','.','#','.','#','.'],	# (r) - red piece
					 #['.','#','.','#','.','#','.','#'],	# (b) - black piece
					 #['#','.','#','R','#','.','#','.'],	# (#) - unplayable slot
					 #['.','#','.','#','.','#','.','#'],	# (.) - free slot
					 #['#','.','#','.','#','.','#','.'],	# (R) - red checker piece
					 #['.','#','.','#','B','#','.','#'],	# (B) - black checker piece
					 #['#','.','#','.','#','.','#','.'],
					 #['.','#','.','#','.','#','.','#']]
		
		self.selected_piece = None	# Set the selected piece
		self.board_image = pygame.image.load(file_name).convert()
		self.red_pieces = []
		self.black_pieces = []
		
		self.TILE_X = self.board_image.get_size()[0]/8 		# number of pixels on x
		self.TILE_Y = self.board_image.get_size()[1]/8 		# number of pixels on y
		
		# Start the pieces on board
		for row in range(len(BOARD_MAP)):
			for col in range(len(BOARD_MAP[0])):
				if BOARD_MAP[row][col] == 'r':
					p = Piece(self.RED_DEFAULT,(row,col),'r')
					p.set_images(self.RED_DEFAULT, self.RED_DEFAULT_SELECTED)
					self.red_pieces.append(p)
					
				if BOARD_MAP[row][col] == 'b':
					p = Piece(self.BLACK_DEFAULT,(row,col),'b')
					p.set_images(self.BLACK_DEFAULT, self.BLACK_DEFAULT_SELECTED)
					self.black_pieces.append(p)
				
				if BOARD_MAP[row][col] == 'R':										# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
					p = Piece(self.RED_CHECKER,(row,col),'R')
					p.set_images(self.RED_CHECKER, self.RED_CHECKER_SELECTED)
					self.red_pieces.append(p)
				if BOARD_MAP[row][col] == 'B':
					p = Piece(self.BLACK_CHECKER,(row,col),'B')
					p.set_images(self.BLACK_CHECKER, self.BLACK_CHECKER_SELECTED)
					self.black_pieces.append(p)										# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	
	
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(-1)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:	# left button
					if(self.RED_TURN):	# red turn to select one piece
						if not self.selected_piece:
							self.select_piece(self.red_pieces)
						else:
							self.move_piece(self.selected_piece)
					
					elif(not self.RED_TURN): # black turn to select one piece
						if not self.selected_piece:
							self.select_piece(self.black_pieces)
						else:
							self.move_piece(self.selected_piece)
						
	
	
	def select_piece(self,pieces):
		pieces_cap,moves,captures = [],[],[]
		piece = None
		for p in pieces:
			m,c = p.generate_moves()
			if len(c) > 0:
				pieces_cap.append(p)
				moves.append(m)
				captures.append(c)
			if p.rect.collidepoint(pygame.mouse.get_pos()):
				piece = p
		if len(captures) > 0:
			if piece in pieces_cap:
				self.selected_piece = piece
				self.selected_piece.set_image_selected()
			else:
				print "Peca Invalida"
				return
		elif piece != None:
			self.selected_piece = piece
			self.selected_piece.set_image_selected()
		else:
			print "selecione uma peca"
			return
			
				
		printBoardMap()
		print self.selected_piece.generate_moves()[0]		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
				
	
	
	def move_piece(self,piece):
		x_m,y_m = pygame.mouse.get_pos()
		col = x_m/self.TILE_X
		row = y_m/self.TILE_Y
		
		if  self.selected_piece.rect.collidepoint(pygame.mouse.get_pos()):
			self.selected_piece.set_image_default()
			self.selected_piece = None
		else:
			i = self.selected_piece.is_next_move(row,col)
			if i >= 0:
				x_p, y_p = self.selected_piece.position
				
				m,c = self.selected_piece.generate_moves()
				if len(c):
					self.remove_piece(c[i])
				
				self.selected_piece.position = (row,col)
				
				if self.selected_piece.group == 'r':
					if self.selected_piece.position[0] == 7:
						self.selected_piece.promote(self.RED_CHECKER, self.RED_CHECKER_SELECTED)
				elif self.selected_piece.group == 'b':
					if self.selected_piece.position[0] == 0:
						self.selected_piece.promote(self.BLACK_CHECKER, self.BLACK_CHECKER_SELECTED)
				
				BOARD_MAP[row][col] = self.selected_piece.group
				BOARD_MAP[x_p][y_p] = '.'
				self.selected_piece.set_image_default()
				self.selected_piece = None
				self.RED_TURN = not self.RED_TURN
			else:
				print "Jogada Invalida"
				return
		#printBoardMap()
	
	
	def remove_piece(self, pos):
		if self.RED_TURN:
			pieces = self.black_pieces
		else: pieces = self.red_pieces
		for p in pieces:
			if p.position == pos:
				pieces.remove(p)
				BOARD_MAP[pos[0]][pos[1]] = '.'
				break
	
	def update(self,screen):
		for piece in self.red_pieces:
			x,y = piece.position
			piece.rect = screen.blit(piece.surface,(y*self.TILE_Y,x*self.TILE_X))
		
		for piece in self.black_pieces:
			x,y = piece.position
			piece.rect = screen.blit(piece.surface,(y*self.TILE_Y,x*self.TILE_X))
	

class Piece(object):
	def __init__(self,surface,pos,group):
		global BOARD_MAP
		self.surface = surface
		self.position = pos
		self.group = group
		self.rect = None
		
	def set_images(self,default,selected):
		""" Define the images for a piece """
		self.default_image = default
		self.selected_image = selected
	
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
	
	def promote(self, default, selected):
		self.set_images(default, selected)
		if self.group == 'r':
			self.group = 'R'
		elif self.group == 'b':
			self.group = 'B'
	
	def generate_moves(self):
		moves = []
		captures = []
		row,col = self.position
		if BOARD_MAP[row][col] == 'r':
			new_row = row + 1
			new_col = col + 1
			if new_col < 8:
				new_position = BOARD_MAP[new_row][new_col]
				if new_position == '.' and len(captures) == 0:
					moves.append((new_row,new_col))
				elif new_position == 'b' or new_position == 'B':
					new_row += 1
					new_col += 1
					if new_row < 8 and new_col < 8:
						new_position = BOARD_MAP[new_row][new_col]
						if new_position == '.':
							if len(captures) == 0:
								moves = []
							captures.append((new_row-1,new_col-1))
							moves.append((new_row,new_col))
			
			new_row = row + 1
			new_col = col - 1
			if new_col >= 0:
				new_position = BOARD_MAP[new_row][new_col]
				if new_position == '.' and len(captures) == 0:
					moves.append((new_row,new_col))
				elif new_position == 'b' or new_position == 'B':
					new_row += 1
					new_col -= 1
					if new_row < 8 and new_col >= 0:
						new_position = BOARD_MAP[new_row][new_col]
						if new_position == '.':
							if len(captures) == 0:
								moves = []
							captures.append((new_row-1,new_col+1))
							moves.append((new_row,new_col))
		
		
		elif BOARD_MAP[row][col] == 'b':
			new_row = row - 1
			new_col = col + 1
			if new_col < 8:
				new_position = BOARD_MAP[new_row][new_col]
				if new_position == '.' and len(captures) == 0:
					moves.append((new_row,new_col))
				elif new_position == 'r' or new_position == 'R':
					new_row -= 1
					new_col += 1
					if new_row >= 0 and new_col < 8:
						new_position = BOARD_MAP[new_row][new_col]
						if new_position == '.':
							if len(captures) == 0:
								moves = []
							captures.append((new_row+1,new_col-1))
							moves.append((new_row,new_col))
			
			new_row = row - 1
			new_col = col - 1
			if new_col >= 0:
				new_position = BOARD_MAP[new_row][new_col]
				if new_position == '.' and len(captures) == 0:
					moves.append((new_row,new_col))
				elif new_position == 'r' or new_position == 'R':
					new_row -= 1
					new_col -= 1
					if new_row >= 0 and new_col >= 0:
						new_position = BOARD_MAP[new_row][new_col]
						if new_position == '.':
							if len(captures) == 0:
								moves = []
							captures.append((new_row+1,new_col+1))
							moves.append((new_row,new_col))
		
		elif BOARD_MAP[row][col] == 'R' or BOARD_MAP[row][col] == 'B':
			new_row = row + 1
			new_col = col + 1
			while( new_row < 8 and new_col < 8):
				moves.append((new_row,new_col))
				new_row += 1
				new_col += 1
			
			new_row = row + 1
			new_col = col - 1
			while( new_row < 8 and new_col >= 0):
				moves.append((new_row,new_col))
				new_row += 1
				new_col -= 1
			
			new_row = row - 1
			new_col = col - 1
			while( new_row >= 0 and new_col >= 0):
				moves.append((new_row,new_col))
				new_row -= 1
				new_col -= 1
			
			new_row = row - 1
			new_col = col + 1
			while( new_row >= 0 and new_col < 8):
				moves.append((new_row,new_col))
				new_row -= 1
				new_col += 1
		
		return moves,captures
	#-- generate_moves() ---------------------------------


if __name__ == "__main__":
	pygame.init()
	pygame.display.set_caption("Checkers")
	
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
	