# Javier Acevedo 1/29/2018
# Just a tic tac toe clone

import os, numpy, pygame, math

class TicTacToe:

    def __init__(self):
        self.gametrix = None
        self.current_player = "X"

        # Game control variables
        self.end_game = False
        self.winner = False

        # Font Settings
        pygame.font.init()

        # Winner font
        self.winner_font = pygame.font.SysFont("monospace", 30)
        self.winner_font.set_bold(True)

        # Restart font
        self.restart_font = pygame.font.SysFont("monospace", 15)
        self.restart_font.set_bold(True)

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Window Settings and Initialization
        self.background_color = (255, 255, 255)
        self.width = 500
        self.height = 500
        self.game_caption = "Tic Tac Toe"


        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_width = self.screen.get_size()[0]
        self.screen_height = self.screen.get_size()[1]
        self.screen.fill(self.background_color)

        pygame.display.set_caption(self.game_caption);
        pygame.display.flip()
        
        self.__init_board()



    def __insert(self, value, pos_x, pos_y):
        # if pos_x < 1 or pos_y < 1: return False
        """ Inserts a given value in a cell prevents cell overrides and shows a message if such scenario is present"""
        if self.gametrix[pos_x][pos_y] is  "0":
            self.gametrix[pos_x][pos_y] = value
        else:
            return False

        #self.__show_matrix()
        return True


    def __init_board(self, restart=False):
        # Initialize game matrix
        self.gametrix = [["0" for x in range(3)] for y in range(3)]
        self.__draw_grid((0, 0, 0), 6)
        pygame.display.flip()


    def __restart_board(self, wait):
        if wait:
            pygame.time.delay(1000)

        self.gametrix = [["0" for x in range(3)] for y in range(3)]

        self.screen.fill(self.WHITE)

        # Draw grid on the screen
        self.__draw_grid((0, 0, 0), 10)
        self.end_game = False

        pygame.display.flip()



    def __update_grid(self):
        matrix_len = len(self.gametrix)
        for i in range(matrix_len):
            for j in range(matrix_len):
                #print "({},{}) : {}".format(i, j, self.gametrix[j][i])

                # This basicly converts the cell (x,y) to its equivalent in the board grid, by 
                # interpolating the cell values to (0,300), the min and max of a 3x3 board
                cell_center_x = int(numpy.interp(i, [0, 2], [0, self.width]))
                cell_center_y = int(numpy.interp(j, [0, 2], [0, self.height]))

                # Calculate center to draw circle
                if (cell_center_x < self.width/3):
                    cell_center_x = ((self.width/3) - ((self.width/3) / 2))
                    #print "KLK: " + str(cell_center_x)
                elif (cell_center_x >= self.width/3 and cell_center_x < self.width/3 * 2):
                    cell_center_x = ((self.width/3) + ((self.width/3) / 2))
                elif (cell_center_x >= self.width/3 * 2):
                    cell_center_x = ((self.width/3 * 2) + ((self.width/3) / 2))

                if (cell_center_y < self.width/3):
                    cell_center_y = ((self.width/3) - ((self.width/3) / 2))
                elif (cell_center_y >= self.width/3 and cell_center_y < self.width/3 * 2):
                    cell_center_y = ((self.width/3) + ((self.width/3) / 2))
                elif (cell_center_y >= self.width/3 * 2):
                    cell_center_y = ((self.width/3 * 2) + ((self.width/3) / 2))

                #print cell_center_x, cell_center_y


                # Calculate the y values of the corner points in the current cell
                # to draw the cross
                if (cell_center_x < 100):
                    cell_corner_point_a_x = 0
                    cell_corner_point_b_x = 100
                elif (cell_center_x >= 100 and cell_center_x < 200):
                    cell_corner_point_a_x = 100
                    cell_corner_point_b_x = 200
                elif (cell_center_x >= 200):
                    cell_corner_point_a_x = 200
                    cell_corner_point_b_x = 300

                # Calculate the y values of the corner points in the current cell
                # to draw the cross
                if (cell_center_y < 100):
                    cell_corner_point_a_y = 0
                    cell_corner_point_b_y = 100
                elif (cell_center_y >= 100 and cell_center_y < 200):
                    cell_corner_point_a_y = 100
                    cell_corner_point_b_y = 200
                elif (cell_center_y >= 200):
                    cell_corner_point_a_y = 200
                    cell_corner_point_b_y = 300



                cell_center_point_a = ((cell_corner_point_a_x, cell_corner_point_a_y))
                cell_center_point_b = ((cell_corner_point_b_x, cell_corner_point_b_y))


                if self.gametrix[j][i] == "O":
                    self.__draw_circle(self.RED, (cell_center_x,cell_center_y))
                elif self.gametrix[j][i] == "X":
                    self.__draw_circle(self.BLUE, (cell_center_x,cell_center_y))
                    #self.__draw_cross(cell_center_point_a, cell_center_point_b)

        pygame.display.flip()


    def __check_win(self, cell_x, cell_y, matrix):
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

    def __check_draw(self):
        gametrix_len = len(self.gametrix)
        for i in range(gametrix_len):
            for j in range(gametrix_len):
                current_cell = self.gametrix[i][j]
                # if any of the cells in the 2d array is 0 it means that there is still not a draw
                # not the most efficient way of checking if there is a draw but it works :D
                if (current_cell == "0"):
                    return False
        # If an empty cell was never found on the 2d array , we can assume
        # that there is a draw.
        return True


    def __draw_grid(self, color, lines_width):
        ### Draws a 3x3 grid on the screen

        pygame.draw.line(self.screen, color, [self.width/3, 0], [self.width/3, self.height], lines_width)
        pygame.draw.line(self.screen, color, [self.width/3 * 2, 0], [self.width/3 * 2, self.height], lines_width)
        pygame.draw.line(self.screen, color, [0, self.height/3], [self.width, self.height/3], lines_width)
        pygame.draw.line(self.screen, color, [0, self.height/3 * 2], [self.width, self.height/3 * 2], lines_width)


    def __draw_circle(self, color, position):
        pygame.draw.circle(self.screen, color, position, 50, 5)


    def __draw_cross(self, p1, p2):
        pygame.draw.line(self.screen, self.BLACK, p1, p2, 6)
        pygame.draw.line(self.screen, self.BLACK, (p1[0] + 100, p1[1] ), (p2[0] - 100, p1[1] + 100), 6)


    def __draw_win(self, winner):
        # Shows the winner on the screen
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        win_text = self.winner_font.render("{} You Win!!".format(self.current_player), 1, self.WHITE)
        restart_text = self.restart_font.render("Press (Space) to restart", 1, self.RED)

        self.screen.blit(win_text, ((self.screen_width * 0.5) - win_text.get_width() * 0.5, (self.screen_height * 0.5 ) - win_text.get_height() * 0.5))
        self.screen.blit(restart_text, ((self.screen_width * 0.5) - restart_text.get_width() * 0.5, (self.screen_height) * 0.6 ))
        pygame.display.flip()

    def __draw_draw(self):
        # Draws Draw on the screen
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        draw_text = self.winner_font.render("Draw".format(self.current_player), 1, self.WHITE)
        restart_text = self.restart_font.render("Press (Space) to restart", 1, self.RED)

        self.screen.blit(draw_text, ((self.screen_width * 0.5) - draw_text.get_width() * 0.5, (self.screen_height * 0.5 ) - draw_text.get_height() * 0.5))
        self.screen.blit(restart_text, ((self.screen_width * 0.5) - restart_text.get_width() * 0.5, (self.screen_height) * 0.6 ))

        pygame.display.flip()


        
    def __switch_turn(self):
        if (self.current_player == "O"):
            self.current_player = "X"
        else:
            self.current_player = "O"
        pass


    def start_game(self):

        running = True
        lmb_pressed = False;
        
        # Main Loop
        while running:

            # When a MOUSEBUTTONDOWN / RMB event occurs, use the current mouse position (which we store on the 
            # MOUSEBUTTONDOWN event ), so we can then check in which cell the player is currently on and place 
            # that value into the 2d array and draw it on the gui matrix as well. 
            # Note: Decided to implement the logic out here instead of the event itself because it is cleaner
            # this way.

            if lmb_pressed:
                mouse_x, mouse_y = self.mouse_pos[0], self.mouse_pos[1]

                lmb_pressed = True

                cell_position = (0, 0)

                # Row 1 events
                if (mouse_x < self.width/3 and mouse_y < self.height/3):
                    cell_position = 0, 0
                elif ((mouse_x > self.width/3 and mouse_x < self.width/3 * 2) and mouse_y < self.height/3):
                    cell_position = 0, 1
                elif (mouse_x > self.width/3 * 2 and mouse_y <  self.height/3):
                    cell_position = 0, 2

                # Row 2 events
                if (mouse_x < self.width/3 and (mouse_y > self.height/3 and mouse_y < self.height/3 * 2)):
                    cell_position = 1, 0
                elif ((mouse_x > self.width/3 and mouse_x < self.width/3 * 2) and (mouse_y > self.height/3 and mouse_y < self.height/3 * 2)):
                    cell_position = 1, 1
                elif (mouse_x > self.width/3 * 2 and (mouse_y > self.height/3 and mouse_y < self.height/3 * 2)):
                    cell_position = 1, 2


                # Row 3 events
                if (mouse_x < self.width/3 and mouse_y > self.height/3 * 2):
                    cell_position = 2, 0
                elif ((mouse_x > self.width/3 and mouse_x < self.width/3 * 2) and mouse_y > self.height/3 * 2):
                    cell_position = 2, 1
                elif (mouse_x > self.width/3 * 2 and mouse_y >  self.height/3 * 2):
                    cell_position = 2, 2


                # Try to insert a move in the game matrix                   
                inserted = self.__insert(self.current_player, cell_position[0], cell_position[1]) 

                # If move could be inserted check if it is a winning move, if not tell the current player
                # to try again
                
                if inserted:
                    # Update the grid everytime a move is inserted
                    self.__update_grid()

                    # Check if the winning conditions have been met
                    win = self.__check_win(cell_position[0], cell_position[1], self.gametrix);
                    #win = False
                    if win:
                        self.winner = True
                        self.end_game = True
                        self.__draw_win("X")
                        
                    else:
                        draw = self.__check_draw()    
                        if draw:   
                            self.end_game = True
                            self.__draw_draw()
                        self.__switch_turn()

                lmb_pressed = False


            # Event Handlinng
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.end_game != True:
                    # When a MOUSEBUTTONDOWN / RMB event occurs, get the current mouse position, so we can
                    # then check in which cell the player is currently on and place that value into the 
                    # 2d array and draw it on the gui matrix as well
                    self.mouse_pos = pygame.mouse.get_pos()
                    lmb_pressed = True

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.end_game:
                        self.end_game = False
                        self.__restart_board(False)

T = TicTacToe()
T.start_game()
