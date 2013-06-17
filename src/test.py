#! -*- coding:utf-8 -*-

from checkers import *
from minimax import *
import pygame,time

base = [[]]*21

#---------[ Início de Jogo ]---------------------------
# Teste com 9 a 12 pecas por jogador

base[0] = [ ['#','b','#','b','#','b','#','b'],
			['b','#','b','#','b','#','b','#'],
			['#','b','#','b','#','b','#','b'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['r','#','r','#','r','#','r','#'],
			['#','r','#','r','#','r','#','r'],
			['r','#','r','#','r','#','r','#']
		  ]

base[1] = [ ['#','.','#','.','#','.','#','.'],
			['.','#','.','#','b','#','b','#'],
			['#','.','#','b','#','.','#','.'],
			['b','#','r','#','b','#','b','#'],
			['#','r','#','.','#','.','#','.'],
			['b','#','r','#','.','#','r','#'],
			['#','.','#','r','#','.','#','.'],
			['.','#','r','#','.','#','R','#']
		  ]

base[2] = [ ['#','b','#','b','#','b','#','b'],
			['.','#','.','#','.','#','b','#'],
			['#','.','#','b','#','b','#','b'],
			['.','#','b','#','.','#','.','#'],
			['#','.','#','.','#','r','#','.'],
			['r','#','b','#','r','#','r','#'],
			['#','.','#','.','#','r','#','r'],
			['r','#','r','#','r','#','.','#']
		  ]

base[3] = [ ['#','b','#','b','#','b','#','b'],
			['.','#','b','#','.','#','b','#'],
			['#','b','#','b','#','b','#','b'],
			['.','#','.','#','b','#','.','#'],
			['#','.','#','r','#','r','#','.'],
			['r','#','r','#','.','#','r','#'],
			['#','.','#','r','#','r','#','r'],
			['r','#','r','#','r','#','.','#']
		  ]

base[4] = [ ['#','.','#','b','#','b','#','b'],
			['.','#','.','#','.','#','b','#'],
			['#','b','#','b','#','b','#','.'],
			['b','#','r','#','.','#','b','#'],
			['#','.','#','.','#','.','#','r'],
			['r','#','r','#','.','#','.','#'],
			['#','r','#','r','#','.','#','r'],
			['.','#','.','#','r','#','r','#']
		  ]

base[5] = [ ['#','.','#','.','#','B','#','.'],
			['b','#','.','#','.','#','b','#'],
			['#','.','#','b','#','b','#','b'],
			['b','#','b','#','b','#','.','#'],
			['#','r','#','.','#','r','#','r'],
			['.','#','r','#','r','#','r','#'],
			['#','.','#','.','#','r','#','.'],
			['.','#','r','#','r','#','r','#']
		  ]

base[6] = [ ['#','b','#','b','#','.','#','.'],
			['.','#','b','#','b','#','b','#'],
			['#','.','#','.','#','b','#','b'],
			['b','#','r','#','.','#','.','#'],
			['#','.','#','.','#','.','#','b'],
			['r','#','r','#','.','#','.','#'],
			['#','r','#','.','#','r','#','r'],
			['r','#','.','#','.','#','r','#']
		  ]


#---------[ Meio de Jogo ]-----------------------------
# Teste com 5 a 8 pecas por jogador

base[7] = [ ['#','b','#','.','#','.','#','b'],
			['r','#','.','#','.','#','b','#'],
			['#','.','#','.','#','b','#','.'],
			['.','#','.','#','.','#','b','#'],
			['#','.','#','.','#','.','#','r'],
			['.','#','.','#','.','#','.','#'],
			['#','r','#','r','#','r','#','.'],
			['.','#','.','#','.','#','.','#']
		  ]

base[8] = [ ['#','b','#','.','#','.','#','b'],
			['b','#','.','#','.','#','b','#'],
			['#','.','#','.','#','b','#','b'],
			['.','#','.','#','b','#','b','#'],
			['#','.','#','.','#','.','#','.'],
			['r','#','r','#','.','#','.','#'],
			['#','r','#','.','#','r','#','r'],
			['.','#','r','#','r','#','r','#']
		  ]

base[9] = [ ['#','.','#','.','#','.','#','.'],
			['.','#','b','#','.','#','.','#'],
			['#','.','#','.','#','b','#','b'],
			['b','#','b','#','.','#','.','#'],
			['#','.','#','.','#','r','#','r'],
			['r','#','r','#','r','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#']
		  ]

base[10] = [['#','.','#','b','#','b','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','r','#','r','#','.'],
			['b','#','.','#','.','#','r','#'],
			['#','.','#','.','#','.','#','r'],
			['.','#','b','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','r','#','.','#','B','#']
		  ]

base[11] = [['#','.','#','b','#','.','#','.'],
			['b','#','b','#','.','#','.','#'],
			['#','b','#','.','#','.','#','b'],
			['r','#','b','#','.','#','.','#'],
			['#','.','#','.','#','r','#','r'],
			['r','#','r','#','b','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['r','#','.','#','r','#','.','#']
		  ]

base[12] = [['#','b','#','.','#','b','#','.'],
			['.','#','b','#','.','#','.','#'],
			['#','b','#','b','#','.','#','b'],
			['r','#','.','#','.','#','b','#'],
			['#','.','#','r','#','b','#','.'],
			['r','#','.','#','r','#','.','#'],
			['#','.','#','r','#','r','#','r'],
			['.','#','.','#','.','#','r','#']
		  ]

base[13] = [['#','.','#','.','#','b','#','.'],
			['b','#','R','#','.','#','r','#'],
			['#','.','#','.','#','.','#','.'],
			['r','#','.','#','B','#','b','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','b','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','r','#','r','#','.','#']
		  ]


#---------[ Fim de Jogo ]------------------------------
# Teste com 1 a 4 pecas por jogador

base[14] = [['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','.','#','b','#','b'],
			['.','#','.','#','.','#','b','#'],
			['#','.','#','.','#','.','#','r'],
			['.','#','b','#','.','#','r','#'],
			['#','.','#','.','#','r','#','.'],
			['.','#','r','#','.','#','.','#']
		  ]

base[15] = [['#','.','#','.','#','.','#','.'],
			['r','#','.','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','b','#','b','#','.','#','.'],
			['.','#','r','#','.','#','b','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#']
		  ]

base[16] = [['#','.','#','.','#','.','#','.'],
			['.','#','b','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','r','#','.','#','.','#','b'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['r','#','.','#','.','#','.','#']
		  ]
base[17] = [['#','.','#','.','#','b','#','.'],
			['r','#','.','#','.','#','.','#'],
			['#','.','#','.','#','.','#','b'],
			['.','#','.','#','.','#','b','#'],
			['#','.','#','.','#','.','#','.'],
			['b','#','.','#','.','#','.','#'],
			['#','.','#','r','#','r','#','r'],
			['.','#','.','#','.','#','.','#']
		  ]
base[18] = [['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','b','#','.','#','.'],
			['b','#','.','#','.','#','b','#'],
			['#','b','#','.','#','.','#','.'],
			['r','#','.','#','.','#','r','#'],
			['#','.','#','.','#','r','#','.'],
			['.','#','.','#','.','#','r','#']
		  ]
base[19] = [['#','.','#','.','#','.','#','.'],
			['B','#','.','#','R','#','.','#'],
			['#','.','#','R','#','.','#','.'],
			['.','#','r','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','r','#']
		  ]

base[20] = [['#','.','#','.','#','.','#','.'],
			['.','#','.','#','.','#','b','#'],
			['#','.','#','b','#','.','#','.'],
			['.','#','.','#','.','#','.','#'],
			['#','.','#','.','#','.','#','b'],
			['.','#','.','#','r','#','.','#'],
			['#','.','#','R','#','.','#','.'],
			['.','#','.','#','.','#','.','#']
		  ]


def gerar_estado(tabuleiro):
	vermelhas = []
	pretas = []
	
	for i, lin in enumerate(tabuleiro):
		for j, casa in enumerate(lin):
			if casa == 'r':
				p = RedPiece((i,j))
				vermelhas.append(p)
			if casa == 'b':
				p = BlackPiece((i,j))
				pretas.append(p)
			
			if casa == 'R':
				p = RedPiece((i,j))
				p.promote()
				vermelhas.append(p)
			if casa == 'B':
				p = BlackPiece((i,j))
				p.promote()
				pretas.append(p)
	
	return Estado(vermelhas,pretas,tabuleiro)


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
	
	
	#for i,board in enumerate(base):
		#print "\nTabuleiro",i
		#for l in board:
			#print l
	
	#--[ Heuristica ]----------------------------------------------------#
	#nivel = [3,5,7,10]
	#heuristica = ["posicional","avanco","avanco2"]
	#for n in nivel:
		#print "===============[ Nível:",n,"]==============="
		#for h1 in heuristica:
			#for h2 in heuristica:
				#print "---------------[",h1," x ",h2,"]---------------"
				#c.start_computer_checkers(minimax_depth=n,
				                           #red_heur=h1,
				                           #black_heur=h2)
	
	#--[ Minimax ]-------------------------------------------------------#
	tempo_inicio = time.time()
	while time.time() - tempo_inicio > 15:
		pass
	
	nivel = [3]#,5]#,7,10]
	heuristica = ["posicional","avanco","avanco2"]
	
	
	keys = ['heuristica','profundidade','estados','tempo']
	resultado_minimax   = [[[{}.fromkeys(keys,['NADA']) for j in range(len(heuristica))]for k in range(len(nivel))] for i in range(len(base))]
	resultado_alfa_beta = [[[{}.fromkeys(keys,['NADA']) for j in range(len(heuristica))]for k in range(len(nivel))] for i in range(len(base))]
	
	for it,tabuleiro in enumerate(base[2:4]):
		print "\n\n==[ Tabuleiro: %d ]=========="%(it)
		
		meu_estado = gerar_estado(tabuleiro)
		
		for ip,n in enumerate(nivel):
			print "_____[ Nível: %d ]______________"%(n)
			for ih, h in enumerate(heuristica):
				print "........[ Heurística: %s ]......."%(h)
				dm = Decisao_Minimax(n,c,h)
				dab= Decisao_Alfa_Beta(n,c,h)
				
				t1_ini = time.time()
				r1 =  dm.comecar_teste(meu_estado,meu_estado.vermelhas,meu_estado.pretas)
				t1_fin = time.time()
				t2_ini = time.time()
				r2 = dab.comecar_teste(meu_estado,meu_estado.vermelhas,meu_estado.pretas)
				t2_fin = time.time()
				print "\tMinimax  :",r1,t1_fin-t1_ini
				resultado_minimax[it][ip][ih]['heuristica'] = h
				resultado_minimax[it][ip][ih]['estados'] = r1
				resultado_minimax[it][ip][ih]['tempo'] = t1_fin-t1_ini
				resultado_minimax[it][ip][ih]['profundidade'] = n
				
				print "\tAlfa-Beta:",r2,t2_fin-t2_ini
				resultado_alfa_beta[it][ip][ih]['heuristica'] = h
				resultado_alfa_beta[it][ip][ih]['estados'] = r2
				resultado_alfa_beta[it][ip][ih]['tempo'] = t2_fin-t2_ini
				resultado_alfa_beta[it][ip][ih]['profundidade'] = n
			
		
		print "==============================="
	
	
	fmm = open("resultado_minimax",'w')
	fab = open("resultado_alfa_beta",'w')
	
	for it, t in enumerate(resultado_minimax):
		for ip, p in enumerate(t):
			for he in p:
				fmm.write("\n------------------")
				fmm.write("\nTabuleiro  "+str(it))
				fmm.write("\nNível      "+str(he['profundidade']))
				fmm.write("\nHeurística "+str(he['heuristica']))
				fmm.write("\nEstados    "+str(he['estados']))
				fmm.write("\nTempo      "+str(he['tempo']))
	
	for it, t in enumerate(resultado_alfa_beta):
		for ip, p in enumerate(t):
			for he in p:
				fab.write("\n------------------")
				fab.write("\nTabuleiro  "+str(it))
				fab.write("\nNível      "+str(he['profundidade']))
				fab.write("\nHeurística "+str(he['heuristica']))
				fab.write("\nEstados    "+str(he['estados']))
				fab.write("\nTempo      "+str(he['tempo']))
	
	
	#--[ Alfa-Beta ]-----------------------------------------------------#
	
	
	