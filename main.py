#-*- coding: utf-8 -*-

from src.checkers import Checkers
from src.minimax  import Minimax
from pygame.locals import *
import src.myMenu as myMenu
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
	
	checkers = Checkers(screen)
	
	state = 0
	while True:
		screen.blit(menu.menu_background,(0,0))
		menu.update()
		
		e = pygame.event.wait()
		
		if e.type == MOUSEMOTION:
			menu.mouse_motion()
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 1 :                           # left button
				if state == 0:                           # current state
					state = menu.mouse_clicked()         # recieve the new state
				
				if state == 1:                           # start game menu
					print "Start Game!"
					menu.set_menu(1)                     # set the menu whith start game options
					state = 0
				elif state == 11:
					print "1 player mode: Easy"
					checkers.start_checkers(minimax_depth=3)
					menu.set_menu(0)
					state = 0
				elif state == 12:
					print "1 player mode: Medium"
					checkers.start_checkers(minimax_depth=5)
					menu.set_menu(0)
					state = 0
				elif state == 13:
					print "1 player mode: Hard"
					checkers.start_checkers(minimax_depth=7)
					menu.set_menu(0)
					state = 0
				elif state == 14:
					print "2 Players Mode"
					checkers.start_checkers()
					menu.set_menu(0)
					state = 0
				elif state == 2:                         # options menu
					print "Menu Options!"
					menu.set_menu(2)                     # set the menu whith options for options menu
					state = 0
				elif state == 3:                         # about menu
					print "About"
					menu.set_menu(3)
					state = 0
				elif state == 6:
					print "Back"
					menu.set_menu(0)
					state = 0
				elif state == 100:
					print "Exit!"
					pygame.quit()
					sys.exit()
		
		if e.type == QUIT:
			pygame.quit()
			sys.exit()
		
		pygame.display.flip()

if __name__ == "__main__": main()