"""
File:    board_square.py
Author:  Sophie Scheck
Date:    11/6/2020
Section: 42
E-mail:  sscheck1@umbc.edu
Description:
  This file contains classes UrPiece and BoardSquare, which create the players pieces
  and the squares on the board as objects with functions like can_move which returns a
  boolean of whether a piece is able to move the number of times their roll provides
"""

WHITE = 'White'
BLACK = 'Black'


class UrPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol
        self.start_pos = None

    def set_start(self, start):
        # this sets the starting position
        self.start_pos = start

    def can_move(self, num_moves):
        """
            This function evaluates if the piece is able to move or if it will 
            be obstructed by another piece on the board or by the exit
        :param num_moves: player's roll
        :return: True or False if the piece is able to move
        """
        # if the player rolls a 0, they cannot move
        if num_moves == 0:
            return False
        from_start = False
        pos = None
        # if the piece's position is None and it has not completed the race,
        # it has not entered the board yet, so pos needs to be set at start
        if self.start_pos and not self.position and not self.complete:
            from_start = True
            pos = self.start_pos
            # setting it to start takes one move for pieces that start off of the board
            num_moves -= 1
        # if the piece already has a position, I set the temp pos to self.position
        if self.position:
            pos = self.position
        # this loop advances the temp pos
        for x in range(num_moves):
            if pos:
                if not pos.exit:
                    if self.color == WHITE:
                        pos = pos.next_white
                    else:
                        pos = pos.next_black
                # this section checks of the piece can successfully move off of the board or not
                elif pos.exit and num_moves - x == 1:
                    return True
                else:
                    return False
        if pos:
            # if the final position does not already have a piece on it, the piece can move to it
            if not pos.piece:
                return True
            # if the final position has a piece of the same color, the piece cannot move to it
            elif pos.piece.color == self.color:
                return False
            # if the previous conditions are false and the final position is not a rosette, the piece can move to it
            elif not pos.rosette:
                return True
        return False

class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
