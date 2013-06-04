# -*- coding:utf-8 -*-

import pygame, sys, os
from pygame.locals import *

BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
WHITE = (255,255,255)

class Menu():
	def __init__(self, screen, font_file = "data/FEASFBRG.TTF", bg_file = "images/menu2.png"):
		self.menu_background = pygame.image.load(bg_file)
		self.menu_font       = pygame.font.Font(font_file,32)
		self.menu_screen     = screen
		self.menu_itens      = []
		self.menu_buttons    = []
		
		self.set_menu(0)
	
	#
	def create_buttons(self,buttons):
		
		self.menu_buttons = []
		itens_height = 0
		
		for b in buttons:
			if b[1] == None:
				new_item = Text(b[0])
			else:
				new_item = Button(b[0],b[1])
				self.menu_buttons.append(new_item)
			
			width, height = self.menu_font.size(b[0])				# Pega o tamanho ocupado pelo texto
			itens_height += height
			
			new_item.rect = pygame.Rect((0,0),(width, height))	# Cria a área ocupada pelo botão
			
			self.menu_itens.append(new_item)
		
		# define as posições dos botões na tela de forma centralizada
		menu_width,menu_height = self.menu_background.get_rect().size
		itens_position = (menu_height - itens_height)/2
		
		for b in self.menu_itens:
			b.center_position(menu_width/2,itens_position)
			itens_position += b.rect.height
	
	
	def set_menu(self,menu_id):
		self.menu_itens = []
		if menu_id == 1:	# Start Menu
			my_itens = [('Vs Computador:',None),
			            ('Facil',           11),
			            ('Medio',           12),
			            ('Dificil',         13),
			            ('',              None),
			            ('Vs Jogador',      14),
			            ('',              None),
			            ('Voltar',           6)]
		elif menu_id == 2:	# Score Menu
			my_itens = [('Pontuacao',     None),
			            ('Voltar',           6)]
		elif menu_id == 3:	# About Menu
			my_itens = [('Regras',        None),
			            ('Voltar',           6)]
		else:				# Main Menu
			my_itens = [('Jogar',     1),
			            ('Pontuacao', 2),
			            ('Regras',    3),
			            ('Sair',    100)]
		
		self.create_buttons(my_itens)
	
	# Change the color buttons when the mouse is on
	def mouse_motion(self):
		m_pos = pygame.mouse.get_pos()
		for b in self.menu_buttons:
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



class MenuItem():
	def __init__(self,text,color):
		self.text              = text        # Texto do botão
		self.color             = color       # Cor padrão do texto
		self.position          = (0,0)       # O botão não sabe onde será desenhado
		self.rect              = None        # O botão não foi desenhado na tela

	def center_position(self,x,y):
		self.rect.center = (x,y)
		self.position = self.rect.topleft

	def draw(self,screen,font):
		b = font.render(self.text,True,self.color)
		self.rect = screen.blit(b,self.position)

class Button(MenuItem):
	def __init__(self,text,action):
		MenuItem.__init__(self,text,BLACK)
		self.action            = action      # Ação (estado) que o botão gera
		self.color_selected    = RED         # Cor padrão do texto do batão selecionado - Vermelho
		self.color_unselected  = BLACK       # Cor padrão do texto do botão - Preta
		self.selected          = False       # Inicialmente o botão não está selecionado
	
	def set_selected(self):
		self.selected = True
		self.color = self.color_selected
	
	def set_unselected(self):
		self.selected = False
		self.color = self.color_unselected
	

class Text(MenuItem):
	def __init__(self,text):
		MenuItem.__init__(self,text,WHITE)
	
	def update_text(self,s):
		self.text = s


