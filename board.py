from tictactoe_sprites import *
import numpy


class Board(object):
  def __init__(self, display_surface, board_dimension, background_color, lines_color):

    # Board properties
    self.BOARD_W, self.BOARD_H = board_dimension

    # Colors
    self.WHITE = (255, 255, 255)
    self.BLACK = (0, 0, 0)

    # Pygame window properties
    self.background_color = background_color
    #self.DSURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    self.DSURFACE = display_surface
    self.DSURFACE.fill(self.background_color)
    self.WIDTH, self.HEIGHT = self.DSURFACE.get_width(), self.DSURFACE.get_height()


    # Registered events list
    self.registered_events = [
    	{"on_cell_lmb_down": []},
    	{"on_cell_rmb_down": []},
    	{"on_space_key_pressed": []}
    ]

    # Grid properties
    self.lines_color = lines_color

    self.sprite_group = pygame.sprite.Group()

    self.running = False

    self.__init_board()

  def __init_board(self):
    #print "Initializing a ({}, {}) board.".format(self.BOARD_W, self.BOARD_H)
    self.board = [["0" for x in range(self.BOARD_W)] for y in range(self.BOARD_H)]

  def restart(self):
    # Clean the 2d array representing the grid
    self.board = [["0" for x in range(3)] for y in range(3)]

    # Remove all sprites from sprite_group to remove them from the screen
    self.sprite_group.empty()
    self.DSURFACE.fill(self.background_color)

    self.__draw_grid(self.lines_color, 1)
		

  def insert_sprite(self, sprite, cell, value_id):
    cell_x, cell_y = cell
    if self.board[cell_x][cell_y] is "0":
      self.board[cell_x][cell_y] = value_id
      x = int(numpy.interp(cell_y, [0, self.BOARD_H], [0, self.WIDTH]))
      y = int(numpy.interp(cell_x, [0, self.BOARD_W], [0, self.HEIGHT]))

      # Set the position of the sprite to the interpolated values x,y (Top left corner of current cell)
      sprite.rect = x, y

      # Scale the image to fit the board size
      sprite.image= pygame.transform.scale(sprite.image, (self.WIDTH/self.BOARD_H, self.HEIGHT/self.BOARD_H))

      # Add sprite to sprite groups and the draw it
      self.sprite_group.add(sprite)
      self.sprite_group.draw(self.DSURFACE)

    else:
      return False
    return True

  def __draw_grid(self, color, lines_width):
    ### Draws a 3x3 grid on the DSURFACE

    # Draw vertical lines
    cell_width = self.WIDTH/self.BOARD_W
    for width in range(cell_width, self.WIDTH, cell_width):
      pygame.draw.line(self.DSURFACE, color, [width, 0], [width, self.HEIGHT], lines_width)

    # Draw horizontal lines
    cell_height = self.HEIGHT/self.BOARD_H
    for height in range(cell_height, self.HEIGHT, cell_height):
      pygame.draw.line(self.DSURFACE, color, [0, height], [self.WIDTH, height], lines_width)

  def get_mouse_pos(self):
    mouse_pos = pygame.mouse.get_pos()
    return mouse_pos

  def register_event(self, function, event_type):
    event = {event_type: function}
    for e in self.registered_events:
      for key, value in e.iteritems():
        if (key == event_type):
          value.append(function)

  def get_registered_events(self, event_name):
    for e in self.registered_events:
      for key, value in e.iteritems():
        if (key == event_name):
          return value

  def on_cell_lmb_down(self, mouse_pos):
    registered_events = self.get_registered_events("on_cell_lmb_down")
    for fn in registered_events:
      fn(mouse_pos)

  def on_cell_rmb_down(self, mouse_pos):
    registered_events = self.get_registered_events("on_cell_rmb_down")
    for fn in registered_events:
      fn(mouse_pos)

  def on_space_key_pressed(self):
    registered_events = self.get_registered_events("on_space_key_pressed")
    for fn in registered_events:
      fn()

  def event_handling(self):
    # Starts event handling for the board grid
    running = True
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pygame.mouse.get_pos()
        cell_center_x = int(numpy.interp(mouse_pos[1], [0, self.WIDTH], [0, self.BOARD_W]))
        cell_center_y = int(numpy.interp(mouse_pos[0], [0, self.HEIGHT], [0, self.BOARD_H]))
        # Call every function registered as lmb_down button , with current mouse pos
        # as argument
        self.on_cell_lmb_down((cell_center_x, cell_center_y))
      elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        mouse_pos = pygame.mouse.get_pos()
        cell_center_x = int(numpy.interp(mouse_pos[1], [0, self.WIDTH], [0, self.BOARD_W]))
        cell_center_y = int(numpy.interp(mouse_pos[0], [0, self.HEIGHT], [0, self.BOARD_H]))
        # Call every function registered as rmb_down button , with current mouse pos
        # as argument
        self.on_cell_rmb_down((cell_center_x, cell_center_y))
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        self.on_space_key_pressed()

  def start(self):
    self.__draw_grid(self.lines_color, 1)
    self.running = True

    while self.running:
      self.event_handling()
      pygame.display.flip()
