"""
Simulation of HGN Test by using a timed dot on the screen.

@author Chase Coleman
@version 11/17/22
"""

import pygame

pygame.init()
screen = pygame.display.set_mode((1700, 1000))
dot = pygame.transform.scale(pygame.image.load("dot.jpeg"), (20, 20))

def  move(clock, positions):
        for position in positions:
           clock.tick(60)
           screen.fill((255, 255, 255))
           screen.blit(dot, (position, 50)) 
           pygame.display.update()

clock = pygame.time.Clock()
screen.fill((255, 255, 255))
screen.blit(dot, (840, 50))
pygame.display.update()

pygame.time.delay(2000)
move(clock, [*range(840, 1, -7)])  
pygame.time.delay(4000)  
move(clock, [*range(1, 1680, 7)])
pygame.time.delay(4000)
move(clock, [*range(1680, 1, -7)])
pygame.time.delay(4000)
move(clock, [*range(1, 1680, 7)])
pygame.time.delay(4000)
move(clock, [*range(1680, 840, -7)])
pygame.time.delay(2000)

pygame.quit()
