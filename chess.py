import pygame
from pygame.locals import *
import random

from piece import Piece
from utils import Utils
from sound import Sound

import os
import time

class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        #play sounds
        try:
            self.sounds = {
                "move": Sound(os.path.join("res", "sounds", "move.wav")),
                "capture": Sound(os.path.join("res", "sounds", "capture.wav"))
            }
        except Exception as e:
            print(f"Error initializing sounds: {e}")
            self.sounds = {}

        # display surface
        self.screen = screen
        # store coordinates of the chess board squares
        self.board_locations = square_coords
        # length of the side of a chess board square
        self.square_length = square_length
        # create an object of class to show chess pieces on the board
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2, scale=1.25)
        self.white_time = 600  # 10 minutes in seconds
        self.black_time = 600
        self.last_update = time.time()
        
        # dictionary to keeping track of player turn
        self.turn = {"black": 0,
                     "white": 0}

        # list containing possible moves for the selected piece
        self.moves = []
        #
        self.utils = Utils()

        # mapping of piece names to index of list containing piece coordinates on spritesheet
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }

        # list containing captured pieces
        self.captured = []
        #
        self.winner = ""

        self.reset()
    
    def reset(self):
        # clear moves lists
        self.moves = []

        # randomize player turn
        #x = random.randint(0, 1)
        #if(x == 1):
            #self.turn["black"] = 1
        #elif(x == 0):
            #self.turn["white"] = 1

        # Always white moves first
        self.turn["white"] = 1
        self.turn["black"] = 0

        # two dimensonal dictionary containing details about each board location
        # storage format is [piece_name, currently_selected, x_y_coordinate]
        self.piece_location = {}
        x = 0
        for i in range(97, 105):
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a>0:
                # [piece name, currently selected, board coordinates]
                self.piece_location[chr(i)][a] = ["", False, [x,y]]
                a = a - 1
                y = y + 1
            x = x + 1

        # reset the board
        for i in range(97, 105):
            x = 8
            while x>0:
                if(x==8):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "black_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "black_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "black_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "black_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "black_king"
                elif(x==7):
                    self.piece_location[chr(i)][x][0] = "black_pawn"
                elif(x==2):
                    self.piece_location[chr(i)][x][0] = "white_pawn"
                elif(x==1):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "white_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "white_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "white_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "white_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "white_king"
                x = x - 1


    # 
    def play_turn(self):
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        small_font = pygame.font.SysFont("argent", 30)
        # create text to be shown on the game menu
        if self.turn["black"]:
            turn_text = small_font.render("Black's Turn", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("White's Turn", True, white_color)
        
        # show welcome text
        self.screen.blit(turn_text, 
                      ((self.screen.get_width() - turn_text.get_width()) // 2,
                      70))
        
        # let player with black piece play
        if(self.turn["black"]):
            self.move_piece("black")
        # let player with white piece play
        elif(self.turn["white"]):
            self.move_piece("white")

    # method to draw pieces on the chess board
    def draw_pieces(self):
        transparent_green = (0,194,39,170)
        transparent_blue = (28,21,212,170)

        # create a transparent surface
        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)

        # loop to change background color of selected piece
        for val in self.piece_location.values():
            for value in val.values() :
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]

                # change background color of piece if it is selected
                if value[1] and len(value[0]) > 5:
                    # if the piece selected is a black piece
                    if value[0][:5] == "black":
                        self.screen.blit(surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface, self.board_locations[x_coord][y_coord])
                    # if the piece selected is a white piece
                    elif value[0][:5] == "white":
                        self.screen.blit(surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface1, self.board_locations[x_coord][y_coord])
        
        # draw all chess pieces
        for val in self.piece_location.values():
            for value in val.values() :
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]
                # check if there is a piece at the square
                if(len(value[0]) > 1):
                    # draw piece on the board
                    self.chess_pieces.draw(self.screen, piece_name, 
                                            self.board_locations[piece_coord_x][piece_coord_y])


    # method to find the possible moves of the selected piece
    def possible_moves(self, piece_name, piece_coord):
        # list to store possible moves of the selected piece
        positions = []
        # find the possible locations to put a piece
        if len(piece_name) > 0:
            # get x, y coordinate
            x_coord, y_coord = piece_coord
            # calculate moves for bishop
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)
            
            # calculate moves for pawn
            elif piece_name[6:] == "pawn":
                # convert list index to dictionary key
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord

                # calculate moves for white pawn
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        # get row in front of black pawn
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]
                
                        # pawns cannot move when blocked by another another pawn
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord+1])
                            # black pawns can move two positions ahead for first move
                            if y_coord < 2:
                                positions.append([x_coord, y_coord+2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1
                            
                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                        # diagonal to the right
                        if x_coord + 1 < 8  and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                # calculate moves for white pawn
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        # get row in front of black pawn
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pawns cannot move when blocked by another another pawn
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord-1])
                            # black pawns can move two positions ahead for first move
                            if y_coord > 5:
                                positions.append([x_coord, y_coord-2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1
                            
                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])

                            
                        # diagonal to the right
                        if x_coord + 1 < 8  and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])


            # calculate moves for rook
            elif piece_name[6:] == "rook":
                # find linear moves
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # calculate moves for knight
            elif piece_name[6:] == "knight":
                # left positions
                if(x_coord - 2) >= 0:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-2, y_coord+1])
                # top positions
                if(y_coord - 2) >= 0:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord-2])
                # right positions
                if(x_coord + 2) < 8:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+2, y_coord+1])
                # bottom positions
                if(y_coord + 2) < 8:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord+2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+2])

            # calculate movs for king
            elif piece_name[6:] == "king":
                if(y_coord - 1) >= 0:
                    # top spot
                    positions.append([x_coord, y_coord-1])

                if(y_coord + 1) < 8:
                    # bottom spot
                    positions.append([x_coord, y_coord+1])

                if(x_coord - 1) >= 0:
                    # left spot
                    positions.append([x_coord-1, y_coord])
                    # top left spot
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-1])
                    # bottom left spot
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-1, y_coord+1])
                    
                if(x_coord + 1) < 8:
                    # right spot
                    positions.append([x_coord+1, y_coord])
                    # top right spot
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+1, y_coord-1])
                    # bottom right spot
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+1])
                
            # calculate movs for queen
            elif piece_name[6:] == "queen":
                # find diagonal positions
                positions = self.diagonal_moves(positions, piece_name, piece_coord)

                # find linear moves
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # list of positions to be removed
            to_remove = []

            # remove positions that overlap other pieces of the current player
            for pos in positions:
                x, y = pos

                # convert list index to dictionary key
                columnChar = chr(97 + x)
                rowNo = 8 - y

                # find the pieces to remove
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if(des_piece_name[:5] == piece_name[:5]):
                    to_remove.append(pos)

            # remove position from positions list
            for i in to_remove:
                positions.remove(i)

        # return list containing possible moves for the selected piece
        return positions

    def update_timers(self, delta_time):
        # Only decrement the timer of the current player
        if self.turn["white"]:
            self.white_time -= delta_time
            if self.white_time <= 0:
                self.white_time = 0
                self.winner = "Black"  # Black wins if White runs out of time
        elif self.turn["black"]:
            self.black_time -= delta_time
            if self.black_time <= 0:
                self.black_time = 0
                self.winner = "White"  # White wins if Black runs out of time


    def draw_timers(self):
        font = pygame.font.SysFont("argent", 28)
        white_time_text = font.render(f"White: {int(self.white_time // 60)}:{int(self.white_time % 60):02}", True, (255, 255, 255))
        black_time_text = font.render(f"Black: {int(self.black_time // 60)}:{int(self.black_time % 60):02}", True, (255, 255, 255))

        # Black timer near top-right, closer to center
        self.screen.blit(
            black_time_text,
            (self.screen.get_width() - black_time_text.get_width() - 75,
             self.screen.get_height() // 2 - 375)
        )

        # White timer near bottom-right, closer to center
        self.screen.blit(
            white_time_text,
            (self.screen.get_width() - white_time_text.get_width() - 75,
             self.screen.get_height() // 2 + 300)
        )



    def move_piece(self, turn):
        # get the coordinates of the square selected on the board
        square = self.get_selected_square()

        # if a square was selected
        if square:
            # get name of piece on the selected square
            piece_name = square[0]
            # color of piece on the selected square
            piece_color = piece_name[:5]
            # board column character
            columnChar = square[1]
            # board row number
            rowNo = square[2]

            # get x, y coordinates
            x, y = self.piece_location[columnChar][rowNo][2]

            # if there's a piece on the selected square
            if(len(piece_name) > 0) and (piece_color == turn):
                # find possible moves for thr piece
                self.moves = self.possible_moves(piece_name, [x,y])

            # checkmate mechanism
            p = self.piece_location[columnChar][rowNo]

            for i in self.moves:
                if i == [x, y]:
                    if(p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x,y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x,y])

            # only the player with the turn gets to play
            if(piece_color == turn):
                # change selection flag from all other pieces
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False

                # change selection flag of the selected piece
                self.piece_location[columnChar][rowNo][1] = True
                
            
    def get_selected_square(self):
        # get left event
        left_click = self.utils.left_click_event()

        # if there's a mouse event
        if left_click:
            # get mouse event
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1], 
                            self.square_length, self.square_length)
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # find x, y coordinates the selected square
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    #reset color of all selected pieces
                                    for val in self.piece_location.values():
                                        for value in val.values() :
                                            # [piece name, currently selected, board coordinates]
                                            if not value[1]:
                                                value[1] = False

                                    # get column character and row number of the chess piece
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # get the name of the 
                                    piece_name = self.piece_location[columnChar][rowNo][0]
                                    
                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None


    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # get x, y coordinate of the destination piece
        x, y = piece_coord

        # get chess board coordinate
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]
        
        if p[0] == "white_king":
            self.winner = "Black"
            print("Black wins")
        elif p[0] == "black_king":
            self.winner = "White"
            print("White wins")

        # Play capture sound if it's not a king (you can add special sound for checkmate later)
        if p[0] not in ["white_king", "black_king"]:
            self.sounds["capture"].play()

        # add the captured piece to list
        self.captured.append(p)
        # move source piece to its destination
        self.validate_move(piece_coord)


    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[1]:
                    # unselect the source piece
                    self.piece_location[k][key][1] = False
                    # get the name of the source piece
                    piece_name = self.piece_location[k][key][0]
                    # move the source piece to the destination piece
                    self.piece_location[desColChar][desRowNo][0] = piece_name
                    
                    src_name = self.piece_location[k][key][0]
                    # remove source piece from its current position
                    self.piece_location[k][key][0] = ""


                    # Play move sound
                    self.sounds["move"].play()

                    # change turn
                    if(self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                        next_color = "white"
                    elif(self.turn["white"]):
                        self.turn["black"] = 1
                        self.turn["white"] = 0
                        next_color = "black"

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print("{} moved from {} to {}".format(src_name,  src_location, des_location))

                    # Check for checkmate after move
                    if self.is_king_in_check(next_color):
                        if self.is_checkmate(next_color):
                            self.winner = "White" if next_color == "black" else "Black"
                            print(f"{self.winner} wins by checkmate!")

    def is_king_in_check(self, color):
        """Returns True if the king of the given color is in check."""
        # Find king's position
        king_pos = None
        for col in self.piece_location:
            for row in self.piece_location[col]:
                piece = self.piece_location[col][row][0]
                if piece == f"{color}_king":
                    king_pos = self.piece_location[col][row][2]
                    break
        if king_pos is None:
            return False  # King not found

        # Check if any enemy piece can move to king's position
        enemy = "white" if color == "black" else "black"
        for col in self.piece_location:
            for row in self.piece_location[col]:
                piece = self.piece_location[col][row][0]
                if piece.startswith(enemy):
                    moves = self.possible_moves(piece, self.piece_location[col][row][2])
                    if king_pos in moves:
                        return True
        return False

    def is_checkmate(self, color):
        """
        Returns True if the player of the given color is in checkmate.
        """
        import copy
        # First, check if the king is in check
        if not self.is_king_in_check(color):
            return False

        # For every piece of this color, see if any legal move gets the king out of check
        for col in self.piece_location:
            for row in self.piece_location[col]:
                piece = self.piece_location[col][row][0]
                if piece.startswith(color):
                    from_pos = self.piece_location[col][row][2]
                    moves = self.possible_moves(piece, from_pos)
                    for move in moves:
                        # Make a deep copy of the board and try the move
                        backup = copy.deepcopy(self.piece_location)
                        # Simulate move
                        dest_col = chr(97 + move[0])
                        dest_row = 8 - move[1]
                        old_piece = self.piece_location[dest_col][dest_row][0]
                        self.piece_location[dest_col][dest_row][0] = piece
                        self.piece_location[col][row][0] = ""
                        # Check if king is still in check
                        in_check = self.is_king_in_check(color)
                        # Undo move
                        self.piece_location = backup
                        if not in_check:
                            return False  # Found a move that escapes check
        return True  # No moves escape check

    def linear_moves(self, positions, piece_name, piece_coord):
        x, y = piece_coord
        color = piece_name.split('_')[0]

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                # Convert to board notation
                col = chr(97 + nx)
                row = 8 - ny
                target_piece = self.piece_location[col][row][0]
                if target_piece == "":
                    positions.append([nx, ny])
                else:
                    if not target_piece.startswith(color):
                        positions.append([nx, ny])
                    break
                nx += dx
                ny += dy
        return positions

    def diagonal_moves(self, positions, piece_name, piece_coord):
        x, y = piece_coord
        color = piece_name.split('_')[0]

        # Directions: top-left, top-right, bottom-left, bottom-right
        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                col = chr(97 + nx)
                row = 8 - ny
                target_piece = self.piece_location[col][row][0]
                if target_piece == "":
                    positions.append([nx, ny])
                else:
                    if not target_piece.startswith(color):
                        positions.append([nx, ny])
                    break
                nx += dx
                ny += dy
        return positions