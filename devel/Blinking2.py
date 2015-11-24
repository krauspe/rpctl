#!/usr/bin/env python

import pygame

# initialize pygame, this must be called before
# doing anything with pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((400, 400))

# setup the text
font = pygame.font.Font(None, 36)
text = font.render("Hello World", True, (100, 100, 100))

display = True

# the main loop
while pygame.time.get_ticks() < 10000: # run the program for 10 seconds
     # empty the screen
     screen.fill((255, 255, 255))

     display = not display

     # draw the text to the screen only if display is True
     if display:
         screen.blit(text, (100, 100))

     # update the actual screen
     pygame.display.flip()

     # wait for half second
     pygame.time.wait(500)
