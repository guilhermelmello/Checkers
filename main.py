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
	
	#buttons = [Button("Exemplo_1",1),
			   ##Button("Exemplo_1",3),
		       #Button("Exemplo_2",2)]
	#buttons[0].set_position(50,50)
	#buttons[1].set_position(50,100)
	##buttons[2].set_position(50,100)
	
	state = 0
	while True:
		screen.blit(menu.menu_background,(0,0))
		menu.update()
		
		#for button in buttons:
			#button.draw(screen,f)
		
		e = pygame.event.wait()
		
		if e.type == MOUSEMOTION:
			menu.mouse_motion()
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 1 :		# botão esquerdo
				if state == 0:
					state = menu.mouse_clicked()
				if state == 1:
					print "Start Game!"
					checkers = Checkers(screen)
					checkers.start_checkers()
					state = 0
				elif state == 2:
					print "Menu Options!"
					state = 0
				elif state == 3:
					print "About"
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