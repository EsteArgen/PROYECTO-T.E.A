
from point import *
import pygame

# Imagenes del sistema 
images =((
      pygame.image.load("asset/1black.png"),
      pygame.image.load("asset/1white.png"),
      pygame.image.load("asset/1blocked.png"),
      pygame.image.load("asset/1empty.png"),
      pygame.image.load("asset/1recommend.png")),(
      pygame.image.load("asset/2black.png"),
      pygame.image.load("asset/2white.png"),
      pygame.image.load("asset/2blocked.png"),
      pygame.image.load("asset/2empty.png"),
      pygame.image.load("asset/2recommend.png"))
    )

# Sprite para trabajar con los mapas de bits del sistema en el tablero 
class square(pygame.sprite.Sprite):
  def __init__(self, pos: point, sts: str):
    super(square, self).__init__()

    #state 
    # 'x' : square is blocked, 
    # '.' : square is empty, 
    # 'w': square is occupied by white Amazon
    # 'b' : square is occupied by black amazon
    # 'r' : square is recommended
    self.state = sts # Bloqueado, vacio
    #pos
    self.pos = pos

    #set team 1
    if self.state == 'w':
      self.image = images[(pos.x + pos.y) % 2][1]
    #set team 2
    elif self.state == 'b':
      self.image = images[(pos.x + pos.y) % 2][0]
    #set other square
    else:
      self.image = images[(pos.x + pos.y) % 2][3]
    
    squareSize = self.image.get_rect().size
    self.rect = pygame.Rect(pos.x * squareSize[0], pos.y * squareSize[1], squareSize[0], squareSize[1])
  
  def recommended(self):
    self.image = images[(self.pos.x + self.pos.y) % 2][4]
    self.state = 'r'

  def clearRecommend(self):
    self.image = images[(self.pos.x + self.pos.y) % 2][3]
    self.state = '.'

  def setQueen(self, player_str):
    if player_str == 'w':
      self.state = 'w'
      self.image = images[(self.pos.x + self.pos.y) % 2][1]
    elif player_str == 'b':
      self.state ='b'
      self.image = images[(self.pos.x + self.pos.y) % 2][0]

    else:
      print("error in square.py, queen function")
  
  def clearQueen(self):
    self.image = images[(self.pos.x + self.pos.y) % 2][3]
    self.state = '.'

  def arrow(self):
    self.image = images[(self.pos.x + self.pos.y) % 2][2]
    self.state = 'x'
  def update(self):
    pass
