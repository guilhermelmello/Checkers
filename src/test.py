#! -*- coding:utf-8 -*-

from checkers import *
from minimax import *
import pygame

if __name__ == "__main__":
	pygame.init()
	font = pygame.font.Font(None,32)
	s = "Iniciando Testes"
	width,height = font.size(s)
	
	screen = pygame.display.set_mode((width+10,height+10))
	
	rect = font.render(s,True,(255,255,255))
	rect = screen.blit(rect,(5,5))
	
	c = Checkers(None)
	
	pygame.display.flip()
	
	#--[ Minimax ]--------------------------------------------------------#
	#m = Minimax(3, c)
	
	#b = [['#','.','#','.','#','.','#','.',],
	     #['.','#','.','#','.','#','.','#',],
	     #['#','.','#','.','#','b','#','b',],
	     #['.','#','.','#','.','#','b','#',],
	     #['#','.','#','.','#','.','#','r',],
	     #['.','#','b','#','.','#','r','#',],
	     #['#','.','#','.','#','r','#','.',],
	     #['.','#','r','#','.','#','.','#',]]
	#reds = []
	#blacks = []
	#for row, lin in enumerate(b):
		#for col, tab in enumerate(lin):
			#if tab == 'r':
				#reds.append(RedPiece((row,col)))
			#elif tab == 'R':
				#p = RedPiece((row,col))
				#p.promote()
				#reds.append(p)
			#elif tab == 'b':
				#blacks.append(BlackPiece((row,col)))
			#elif tab == 'B':
				#p = BlackPiece((row,col))
				#p.promote()
				#blacks.append(p)
	
	#r = m.start_minimax(b,reds,blacks,reverse=True)
	#print r[0].position
	#print r[1]
	#print r[2]
	
	
	#--[ Heuristica ]-----------------------------------------------------#
	
	
	#--[ Confronto Máquina Vs Máquina ]-----------------------------------#
	c.start_computer_checkers(red_heur="default",black_heur="default")
	
	
	
	