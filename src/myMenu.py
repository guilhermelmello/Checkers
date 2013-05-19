# -*- coding:utf-8 -*-

import pygame, sys, os
from pygame.locals import *

BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
WHITE = (255,255,255)

class Menu():
	def __init__(self, screen, font_file = "data/FEASFBRG.TTF", bg_file = "images/menu.png"):
		self.menu_background = pygame.image.load(bg_file)
		self.menu_font       = pygame.font.Font(font_file,32)
		self.menu_screen     = screen
		self.menu_itens      = []
		
		self.set_menu(0)
	
	#
	def create_buttons(self,buttons):
		
		buttons_height = 0
		
		for b in buttons:
			new_button = Button(b[0],b[1])
			
			width, height = self.menu_font.size(b[0])				# Pega o tamanho ocupado pelo texto
			buttons_height += height
			
			new_button.rect = pygame.Rect((0,0),(width, height))	# Cria a área ocupada pelo botão
			
			self.menu_itens.append(new_button)
		
		# define as posições dos botões na tela de forma centralizada
		menu_width,menu_height = self.menu_background.get_rect().size
		button_position = (menu_height - buttons_height)/2
		
		for b in self.menu_itens:
			b.center_position(menu_width/2,button_position)
			button_position += b.rect.height
	
	
	def set_menu(self,menu_id):
		self.menu_itens = []
		if menu_id == 1:	# Start Menu
			my_buttons = [('1 Player Mode',  11),
			              ('2 Players Mode ',12),
			              ('Back',            6)]
		elif menu_id == 2:	# Options Menu
			my_buttons = [('Hard',           21),
			              ('Medium',         22),
			              ('Easy',           23),
			              ('Back',            6)]
		elif menu_id == 3:	# About Menu
			my_buttons = [('Back',            6)]
		else:				# Main Menu
			my_buttons = [('Start',   1),
			              ('Options', 2),
			              ('About',   3),
			              ('Exit',  100)]
		
		self.create_buttons(my_buttons)
	
	# Change the color buttons when the mouse is on
	def mouse_motion(self):
		m_pos = pygame.mouse.get_pos()
		for b in self.menu_itens:
			if b.rect.collidepoint(m_pos):
				b.set_selected()
			else: b.set_unselected()
	
	# Return the state of the selected button
	def mouse_clicked(self):
		m_pos = pygame.mouse.get_pos()
		for b in self.menu_itens:
			if b.rect.collidepoint(m_pos):
				return b.action
		return 0
	
	
	def update(self):
		for item in self.menu_itens:
			item.draw(self.menu_screen,self.menu_font)


class Button():
	def __init__(self,text,action):
		self.text              = text        # Texto do botão
		self.action            = action      # Ação (estado) que o botão gera
		self.selected          = False       # Inicialmente o botão não está selecionado
		self.color_selected    = RED         # Cor padrão do texto do batão selecionado - Vermelho
		self.color_unselected  = BLACK       # Cor padrão do texto do botão - Preta
		self.color             = BLACK       # Cor padrão do texto
		self.position          = (0,0)       # O botão não sabe onde será desenhado
		self.rect              = None        # O botão não foi desenhado na tela
	
	def center_position(self,x,y):
		self.rect.center = (x,y)
		self.position = self.rect.topleft
	
	def set_selected(self):
		self.selected = True
		self.color = self.color_selected
	
	def set_unselected(self):
		self.selected = False
		self.color = self.color_unselected
	
	def draw(self,screen,font):
		b = font.render(self.text,True,self.color)
		self.rect = screen.blit(b,self.position)

