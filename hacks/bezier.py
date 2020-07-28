#!/usr/bin/python
'''Display some animated bezier curves, using SDL'''

__author__ = 'Aaron Brady <bradya@gmail.com>'

import pygame
import time

pygame.init()

window = pygame.display.set_mode((400, 400)) 
screen = pygame.display.get_surface()

C = (128,128,128)

X0 = 100
X1 = 200
X2 = 300
Y0 = 100
Y1 = 100
Y2 = 300

X3 = 300
Y3 = 300

screen.set_at((X0,Y0), C)
screen.set_at((X1,Y1), C)
screen.set_at((X2,Y2), C)
screen.set_at((X3,Y3), C)

def doit(invert=False):
	global X0, X1, X2, X3, Y0, Y1, Y2, Y3, C, screen
	#Y2 = 200 - Y1
	Y1 = 100 + Y1
	if invert:
		Y1 = Y1 - 250
	screen.set_at((X1,Y1), C)
	for i in range(300):
		t = i / 300.0
		P0, P1, P2, P3 = X0, X1, X2, X3
		P = (pow((1.0 - t), 2) * P0) + ((2 * t) * (1 - t) * P1) + (pow(t, 2) * P2)
		X = P
		P0, P1, P2, P3 = Y0, Y1, Y2, Y3
		P = (pow((1.0 - t), 2) * P0) + ((2 * t) * (1 - t) * P1) + (pow(t, 2) * P2)
		Y = P
		screen.set_at((X,Y), C)
	#time.sleep(0.050)

while 1:
	for Y1 in range(100, 200, 1):
		X1 = 100 - (Y1/2)
		X2 = 100 + (Y1*1.1)
		doit()
		X1 = 200 - (Y1/2)
		doit(invert=True)
		pygame.display.flip()
		screen.fill((0,0,0))
	for Y1 in range(200, 100, -1):
		X1 = 100 - (Y1/2)
		X2 = 100 + (Y1*1.1)
		doit()
		X1 = 200 - (Y1/2)
		doit(invert=True)
		pygame.display.flip()
		screen.fill((0,0,0))
