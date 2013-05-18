#-*- coding: utf-8 -*-

from checkers import Checkers
from minimax  import Minimax
from pygame.locals import *
import myMenu
import copy
import pygame
import os, sys

def main():
	
	pygame.init()
	pygame.display.set_caption("myMenu.py")
	
	os.environ['SDL_VIDEO_WINDOW_POS'] = '500,100'
	
	screen = pygame.display.set_mode((0,0))
	
	menu = myMenu.Menu(screen)
	
	screen = pygame.display.set_mode(menu.menu_background.get_size(),0,32)
	
	f = pygame.font.Font("FEASFBRG.TTF",32)
	
	state = 0
	while True:
		screen.blit(menu.menu_background,(0,0))
		menu.update()
		
		e = pygame.event.wait()
		
		if e.type == MOUSEMOTION:
			menu.mouse_motion()
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 1 :		# botão esquerdo
				if state == 0:
					state = menu.mouse_clicked()
				if state == 1:
					print "Start Game!"
					menu.set_menu(1)
					state = 0
				elif state == 2:
					print "Menu Options!"
					menu.set_menu(2)
					state = 0
				elif state == 3:
					print "About"
					menu.set_menu(3)
					state = 0
				elif state == 4:
					print "1 player mode"
					state = 0
				elif state == 5:
					print "2 Players Mode"
					checkers = Checkers(screen)
					checkers.start_checkers()
					state = 0
				elif state == 6:
					print "Back"
					menu.set_menu(0)
					state = 0
				elif state == 10:
					print "Exit!"
					pygame.quit()
					sys.exit()
		
		if e.type == QUIT:
			pygame.quit()
			sys.exit()
		
		pygame.display.flip()

if __name__ == "__main__": main()