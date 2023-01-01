"""
Description:
  This program runs an ancient two player game called
  the Royal Game of Ur
"""

from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece


WHITE = 'White'
BLACK = 'Black'
OFF = 'Off'
COMPLETE = 'Complete'

BOARD_FILE_NAME = 'original_board.ur'


class RoyalGameOfUr:
    STARTING_PIECES = 7

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)
        # keep track of the individual player info
        self.white = {'player': None, 'pieces': [], 'start piece': None, 'end piece': None}
        self.black = {'player': None, 'pieces': [], 'start piece': None, 'end piece': None}
        self.current_player = None
        self.current_pieces = None

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'], rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        NEVER HAS TO BE CALLED
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object
        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def play_game(self):
        """
        This function is where the game functions are organized and ordered
        """
        self.create_players()
        self.create_pieces()
        self.set_start_and_end()

        # runs while a player has not won the game
        end_game = False
        turns_count = 0
        self.display_board()
        while not end_game:
            turns_count += 1
            if turns_count % 2 != 0:
                self.current_player = self.white['player']
                self.current_pieces = self.white['pieces']
            else:
                self.current_player = self.black['player']
                self.current_pieces = self.black['pieces']
            if turns_count > 1:
                self.display_board()
            roll = self.roll_d4_dice()
            print(self.current_player, 'you rolled a', str(roll))
            self.display_pieces(roll)
            self.take_turn(roll)
            end_game = self.end_game_flag()
        if self.current_player == self.white['player']:
            print('Congratulations,', self.white['player'], ', you have won the game!!')
        else:
            print('Congratulations,', self.black['player'], ', you have won the game!!')

    def create_players(self):
        """
            This function prompts the players for names and adds them to their respective dictionary
        """
        self.white['player'] = input('What is your name? ')
        print(self.white['player'], 'you will play as white.')
        self.black['player'] = input('What is your name? ')
        print(self.black['player'], 'you will play as black.')

    def create_pieces(self):
        """
            This function creates the number of pieces set as the constant
            START_PIECES and gives each piece a color and sybmol as an UrPiece object
        """
        for x in range(self.STARTING_PIECES):
            piece_name = 'W' + str(x + 1)
            piece = UrPiece(WHITE, piece_name)
            self.white['pieces'].append(piece)
        for x in range(self.STARTING_PIECES):
            piece_name = 'B' + str(x + 1)
            piece = UrPiece(BLACK, piece_name)
            self.black['pieces'].append(piece)

    def set_start_and_end(self):
        """
            This function establishes the start and end pieces for each color
        """
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y].entrance == WHITE:
                    self.white['start piece'] = self.board[x][y]
                if self.board[x][y].entrance == BLACK:
                    self.black['start piece'] = self.board[x][y]
                if self.board[x][y].exit == WHITE:
                    self.white['end piece'] = self.board[x][y]
                if self.board[x][y].exit == BLACK:
                    self.black['end piece'] = self.board[x][y]

    def take_turn(self, roll):
        """
            This function allows each player to choose a piece to move
        :param roll: the number of moves the player has
        :return:
        """
        piece = None
        finished = False
        extra_turn = False
        # runs until the player has entered a valid integer which can be moved
        while not finished:
            # the boolean extra_turn takes care of the rosette case when the player gains a turn
            if extra_turn:
                extra_turn = False
                roll = self.roll_d4_dice()
                print(self.current_player, 'you rolled a', str(roll))
                self.display_pieces(roll)
            can_move_count = 0
            # counts the number of pieces which can be potentially moved
            # with the number of moves they have rolled
            for x in range(self.STARTING_PIECES):
                check_piece = self.current_pieces[x]
                if check_piece:
                    if not check_piece.position:
                        if self.current_player == self.white['player']:
                            check_piece.start_pos = self.white['start piece']
                        else:
                            check_piece.start_pos = self.black['start piece']
                if self.current_pieces[x].can_move(roll):
                    can_move_count += 1
            # if no pieces can be moved, the players turn is over
            if can_move_count == 0:
                finished = True
                print('No moves are possible with the current dice roll.')
            elif roll == 0:
                finished = True
                print('No moves are possible with the current dice roll.')
            else:
                moving_piece = input('Which move do you wish to make? ')
                # find which piece the player wants to move based on its symbol
                for x in range(self.STARTING_PIECES):
                    for y in range(self.STARTING_PIECES):
                        if self.current_pieces[x].symbol[1] == str(y + 1) and str(y + 1) == moving_piece \
                                and not self.current_pieces[x].complete:
                            piece = self.current_pieces[x]
                if piece:
                    # if the piece does not have a position, this statement sets its position to the start
                    if not piece.position:
                        if self.current_player == self.white['player']:
                            piece.start_pos = self.white['start piece']
                        else:
                            piece.start_pos = self.black['start piece']
                    if not piece.can_move(roll):
                        print('No moves are possible for this piece.')
                    else:
                        # if move returns True, the player has landed on a rosette, so they get another turn
                        if not self.move(roll, piece):
                            finished = True
                        else:
                            extra_turn = True

    def display_pieces(self, num_moves):
        """
            This function displays the potential pieces that the player can move based on the
            number of moves that they rolled
        :param num_moves: this is the players roll
        """
        status = ''
        for x in range(self.STARTING_PIECES):
            piece = self.current_pieces[x]
            # sets the piece's start position
            if piece:
                if not piece.position:
                    if self.current_player == self.white['player']:
                        piece.start_pos = self.white['start piece']
                    else:
                        piece.start_pos = self.black['start piece']
            if piece.can_move(num_moves):
                # if can_move returns True, this statement checks to see if the piece is on or off the board
                if not piece.position and not piece.complete:
                    status = 'currently off the board'
                elif not piece.complete:
                    status = str(piece.position.position)
                print(str(x + 1), piece.symbol, status)
        # checks for pieces that have already completed the race
        for x in range(self.STARTING_PIECES):
            piece = self.current_pieces[x]
            if piece:
                if piece.complete:
                    print(piece.symbol, 'has completed the race.')

    def move(self, roll, piece):
        """
            This function moves the piece the player has selected to its new position on the board
        :param roll: number of moves the player has
        :param piece: the UrPiece which the player has selected to move
        :return: True or False based on if the player has landed on a rosette
        """
        current_square = piece.position
        on_board = False
        if current_square:
            on_board = True
        # if the piece is not on the board, this places the pieces on the start piece
        # and subtracts from their roll by 1
        if not current_square and not on_board:
            if self.current_player == self.white['player']:
                current_square = self.white['start piece']
            else:
                current_square = self.black['start piece']
            roll -= 1
        # runs for the amount of moves a player has
        for x in range(roll):
            if self.current_player == self.white['player']:
                # if the piece is on the last square of the board, the piece's position is changed to None
                if current_square == self.white['end piece']:
                    piece.position.piece = None
                    piece.position = None
                    piece.complete = True
                # if the piece lands on a piece of a different color and it is not on a rosette,
                # it knocks off the other piece and is put in its place
                elif current_square.next_white.piece and current_square.next_white.piece.color != piece.color and \
                        not current_square.next_white.rosette and roll == x + 1:
                    print(current_square.next_white.piece.symbol, 'has been knocked off')
                    current_square.next_white.piece.position = None
                    current_square = current_square.next_white
                # if the piece lands on an empty rosette, the player gets another turn
                # and True is returned so that the player gets another roll within take_turn()
                elif current_square.next_white.rosette and not current_square.next_white.piece and roll == x + 1:
                    current_square = current_square.next_white
                    if piece.position:
                        piece.position.piece = None
                    piece.position = current_square
                    current_square.piece = piece
                    self.display_board()
                    print('You have landed on a rosette. You get another turn!')
                    return True
                # otherwise, the piece advances to the next square
                else:
                    current_square = current_square.next_white
            # same code for black piece
            else:
                if current_square == self.black['end piece']:
                    piece.position.piece = None
                    piece.position = None
                    piece.complete = True
                elif current_square.next_black.piece and current_square.next_black.piece.color != piece.color and \
                        not current_square.next_black.rosette and roll == x + 1:
                    print(current_square.next_black.piece.symbol, 'has been knocked off')
                    current_square.next_black.piece.position = None
                    current_square = current_square.next_black
                elif current_square.next_black.rosette and not current_square.next_black.piece and roll == x + 1:
                    current_square = current_square.next_black
                    if piece.position:
                        piece.position.piece = None
                    piece.position = current_square
                    current_square.piece = piece
                    self.display_board()
                    print('You have landed on a rosette. You get another turn!')
                    return True
                else:
                    current_square = current_square.next_black
        # makes sure that the old BoardSquare does not still have the piece on it,
        # because it has been changed to a new square
        if piece.position and not piece.complete:
            piece.position.piece = None
        # changes the actual piece.position and current_square.piece
        # to where the piece has been moved to
        if current_square and not piece.complete:
            piece.position = current_square
            current_square.piece = piece

    def end_game_flag(self):
        """
            This function checks to see if the all of the player's pieces have set piece.complete to True
        :return: True or False if all of the player's pieces have completed the race
        """
        count = 0
        # counts the number of pieces which have not completed the race
        if self.current_player == self.white['player']:
            for x in range(self.STARTING_PIECES):
                if not self.white['pieces'][x].complete:
                    count += 1
        if self.current_player == self.black['player']:
            for x in range(self.STARTING_PIECES):
                if not self.black['pieces'][x].complete:
                    count += 1
        # if the count is 0, then none of the pieces have yet to finish the race and the player has won
        if count == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    rgu = RoyalGameOfUr(BOARD_FILE_NAME)
    rgu.play_game()
