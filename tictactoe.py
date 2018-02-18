import numpy, pygame
from board import *
from tictactoe_sprites import *


# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

# Fonts
pygame.font.init()
winner_font = pygame.font.SysFont("monospace", 30)
restart_font = pygame.font.SysFont("monospace", 15)

# Window properties
window_dimension = (600, 600)
DSURFACE = pygame.display.set_mode(window_dimension)

# Board properties
background_color = WHITE
grid_lines_color = BLACK

# Tictactoe sprites
cross = Cross()
circle = Circle()

# Initialize a 3x3 gui board
tictactoe_board = Board(DSURFACE, (3, 3), background_color, grid_lines_color)

# Game properties
current_player = "cross"
game_ended = False


### Game control functions ###

def switch_turn():
	global current_player
	if current_player == "cross":
		current_player = "circle"
	else:
		current_player = "cross"

def player_move(current_cell_pos):
	global game_ended
	inserted = False
	if current_player == "cross":
		inserted = tictactoe_board.insert_sprite(cross, current_cell_pos, cross.id)
	elif current_player == "circle":
		inserted = tictactoe_board.insert_sprite(circle, current_cell_pos, circle.id)
	
	if inserted:
		board = tictactoe_board.board
		win = check_win(current_cell_pos[0], current_cell_pos[1], board)
		draw = check_draw(board)
		if win:
			game_ended = True
			draw_win(current_player)
		elif draw:
			game_ended = True
			draw_draw()
		switch_turn()

def check_win(cell_x, cell_y, matrix):
  ### Check is the latest move is the winning move, by analyzing all the possible
  ### winning conditions of the current move/cell.

  ### First identify if the last move was in a edge cell or corner cell, by adding up
  ### the cell x and y, if this sum equals to a even number, the current cell is a 
  ### corner/center, otherwise it's an edge.
  
  matrix_len = len(matrix)
  cell_sum = cell_x + cell_y
  
  row, column, r_diagonal, l_diagonal = ("", "", "", "")

  for i in range(matrix_len):
      # Get the row and column that intersects the current cell 
      row += matrix[cell_x][i]
      column += matrix[i][cell_y]
      # If the sum of x,y of the cell is an even number, it means we are
      # on an edge or the center, so we need to get the diagonal that intersects the current cell
      if (cell_sum % 2  == 0):
          l_diagonal += matrix[i][i]
          r_diagonal += matrix[i][(matrix_len - 1) - i]

  # Winnin condition it's the current player or the current value (X or O) that was placed on the 
  # current cell muliplied by 3. (XXX or 000), basically the winning condition of Tic Tac Toe
  winning_condition = matrix[cell_x][cell_y] * 3

  # row, column, and both diagonals at this point store all the values on of the complete row, column or diagonal
  # that intersect the current cell, then we just have to check if this is equal to the winning condition.
  if row == winning_condition or column == winning_condition or r_diagonal == winning_condition or l_diagonal == winning_condition:
      return True

  return False

def check_draw(board):
  board_len = len(board)
  for i in range(board_len):
      for j in range(board_len):
          current_cell = board[i][j]
          # if any of the cells in the 2d array is 0 it means that there is still not a draw
          # not the most efficient way of checking if there is a draw but it works :D
          if (current_cell == "0"):
              return False
  # If an empty cell was never found on the 2d array , we can assume
  # that there is a draw.
  return True

def restart_game():
	# TODO: actually restart game, for now just quit
	if game_ended:
		tictactoe_board.restart()


### Drawing Functions ###

def draw_draw():
	# Draws Draw on the screen
	overlay = pygame.Surface(DSURFACE.get_size())
	overlay.set_alpha(200)
	overlay.fill(BLACK)
	DSURFACE.blit(overlay, (0, 0))
	draw_text = winner_font.render("DRAW".format(current_player), 1, WHITE)
	restart_text = restart_font.render("Press (Space) to restart", 1, RED)

	DSURFACE.blit(draw_text, ((window_dimension[0] * 0.5) - draw_text.get_width() * 0.5, (window_dimension[1] * 0.5 ) - draw_text.get_height() * 0.5))
	DSURFACE.blit(restart_text, ((window_dimension[0] * 0.5) - restart_text.get_width() * 0.5, (window_dimension[1]) * 0.6 ))

	pygame.display.flip()

def draw_win(winner):
	# Shows the winner on the screen
	overlay = pygame.Surface(DSURFACE.get_size())
	overlay.set_alpha(200)
	overlay.fill(BLACK)
	DSURFACE.blit(overlay, (0, 0))
	win_text = winner_font.render("{} YOU WIN!!".format(current_player.upper()), 1, WHITE)
	restart_text = restart_font.render("Press (Space) to restart", 1, RED)

	DSURFACE.blit(win_text, ((window_dimension[0] * 0.5) - win_text.get_width() * 0.5, (window_dimension[1] * 0.5 ) - win_text.get_height() * 0.5))
	DSURFACE.blit(restart_text, ((window_dimension[0] * 0.5) - restart_text.get_width() * 0.5, (window_dimension[1]) * 0.6 ))
	pygame.display.flip()


# Register board click events
tictactoe_board.register_event(player_move, "on_cell_lmb_down")
tictactoe_board.register_event(restart_game, "on_space_key_pressed")


tictactoe_board.start()

