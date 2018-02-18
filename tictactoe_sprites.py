import pygame
import os, sys
from pygame.locals import *

class Cross(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('sprites/cross.png')
    self.rect = self.image.get_rect()
    self.id = "X"


class Circle(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("sprites/circle.png")
    self.rect = self.image.get_rect()
    self.id = "O"