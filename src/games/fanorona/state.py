from typing import Optional

from games.fanorona.action import FanoronaAction
from games.fanorona.result import FanoronaResult
from games.state import State


class FanoronaState(State):
    WHITE_CELL = 0
    BLACK_CELL = 1
    EMPTY_CELL = -1

    #MOVES
    HORIZONTAL_RIGHT = "horizontal_right"
    HORIZONTAL_LEFT = "horizontal_left"
    VERTICAL_DOWN = "vertical_right"
    VERTICAL_UP = "vertical_up"
    DIAGONAL_DOWN = "diagonal_down"
    DIAGONAL_UP = "diagonal_up"
    INVALID_MOVE = "invalid_move"

    def __init__(self):
        super().__init__()

        """
        the dimensions of the board
        """
        self.__num_rows = 5
        self.__num_cols = 9

        """
        the grid
        """
        self.__grid = [[FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL,FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL,FanoronaState.EMPTY_CELL,FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL,FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL],
                       [FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       ]
        self.__last_move_p0 = None
        self.__last_move_p1 = None
        self.last_piece_pos = None

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player
        """
        self.__acting_player = FanoronaState.WHITE_CELL

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    #!TODO: CHECK WINNER
    def __check_winner(self, player):
        white_pieces = 0
        black_pieces = 0
        for row in range(0,self.__num_rows):
            for col in range(0,self.__num_cols):
                if self.__grid[row][col] == FanoronaState.WHITE_CELL:
                    white_pieces += 1
                elif self.__grid[row][col] == FanoronaState.BLACK_CELL:
                    black_pieces += 1
        if white_pieces == 0 or black_pieces == 0:
            return True
        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: FanoronaAction) -> bool:
        move = self.verify_move(action)
        if self.__grid[action.get_final_x()][action.get_final_y()] != FanoronaState.EMPTY_CELL :
            return False
        if move == FanoronaState.INVALID_MOVE:
            return False
        if self.__acting_player == 0 and move == self.__last_move_p0:
            return False
        if self.__acting_player == 1 and move == self.__last_move_p1:
            return False
        if self.last_piece_pos is not None and self.last_piece_pos != [action.get_final_x(), action.get_final_y()]:
            return False
        if action.get_initial_x() < 0 or action.get_initial_y() < 0 or action.get_final_x() < 0 or action.get_final_y() < 0:
            return False
        if action.get_initial_x() > self.__num_rows or action.get_initial_y() > self.__num_cols \
            or action.get_final_x() > self.__num_rows or action.get_final_y() > self.__num_cols:
            return False

        return True

    def update(self, action: FanoronaAction):
        initial_x = action.get_initial_x()
        initial_y = action.get_initial_y()
        final_x = action.get_final_x()
        final_y = action.get_final_y()
        draw_pieces_down : int = 0
        draw_pieces_up : int= 0
        draw_pieces_left : int = 0
        draw_pieces_right : int = 0
        move = self.verify_move(action)

        if self.__acting_player == 0:
            self.__last_move_p0 = move
        else:
            self.__last_move_p1 = move

        #moves the piece
        self.__grid[final_x][final_y] = self.__grid[initial_x][initial_y]
        self.__grid[initial_x][initial_y] = FanoronaState.EMPTY_CELL

        #capture pieces
        # always in a same direction
        #verifications if the move is diagonal
        if move is FanoronaState.DIAGONAL_UP or FanoronaState.DIAGONAL_DOWN :
            for i in range(final_x + 1,self.get_num_rows()):
                if self.__grid[i][i] != self.__acting_player:
                    draw_pieces_down += 1
                else:
                    break
            for i in range(final_x - 1,-1,-1):
                if self.__grid[i][i] != self.__acting_player:
                    draw_pieces_up += 1
                else:
                    break
            if draw_pieces_up < draw_pieces_down :
                for i in range(final_x + 1, self.get_num_rows()):
                    if self.__grid[i][i] != self.__acting_player:
                        self.__grid[i][i] = FanoronaState.EMPTY_CELL
                    else:
                        break
            if draw_pieces_up > draw_pieces_down :
                for i in range(final_x - 1, -1, -1):
                    if self.__grid[i][i] != self.__acting_player:
                        self.__grid[i][i] = FanoronaState.EMPTY_CELL
                    else:
                        break

        #verifications if the move is vertical
        if move is FanoronaState.VERTICAL_UP or FanoronaState.VERTICAL_DOWN:
            for i in range(final_x + 1, self.__num_rows):
                if self.__grid[i][final_y] != self.__acting_player:
                    draw_pieces_down += 1
                else:
                    break
            for i in range(final_x - 1,-1-1):
                if self.__grid[i][final_y] != self.__acting_player:
                    draw_pieces_up += 1
                else:
                    break
            if draw_pieces_up < draw_pieces_down:
                for i in range(final_x + 1, self.__num_rows):
                    if self.__grid[i][final_y] != self.__acting_player:
                        self.__grid[i][final_y] = FanoronaState.EMPTY_CELL
                    else:
                        break
            if draw_pieces_up > draw_pieces_down:
                for i in range(final_x - 1, -1 - 1):
                    if self.__grid[i][final_y] != self.__acting_player:
                        self.__grid[i][final_y] = FanoronaState.EMPTY_CELL
                    else:
                        break

        #verifications if the move is horizontal
        if move is FanoronaState.HORIZONTAL_LEFT or FanoronaState.HORIZONTAL_RIGHT:
            for i in range(final_y + 1, self.__num_cols):
                if self.__grid[final_x][i] != self.__acting_player:
                    draw_pieces_right += 1
                else:
                    break
            for i in range(final_x -1 , -1, -1):
                if self.__grid[final_x][i] != self.__acting_player:
                    draw_pieces_left += 1
                else:
                    break
            if draw_pieces_right > draw_pieces_left :
                for i in range(final_y + 1, self.__num_cols):
                    if self.__grid[final_x][i] != self.__acting_player:
                        self.__grid[final_x][i] = FanoronaState.EMPTY_CELL
                    else:
                        break
            if draw_pieces_right < draw_pieces_left:
                for i in range(final_x - 1, -1, -1):
                    if self.__grid[final_x][i] != self.__acting_player:
                        draw_pieces_left += 1
                    else:
                        break

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        self.last_piece_pos = [final_x,final_y]
        # switch to next player
        #verify if the player eat pieces if true does not change the player
        if draw_pieces_up == 0 and draw_pieces_down == 0 and draw_pieces_left == 0 and draw_pieces_right == 0:
            self.__acting_player = FanoronaState.BLACK_CELL if self.__acting_player == FanoronaState.WHITE_CELL else FanoronaState.WHITE_CELL
            self.last_piece_pos = None

        self.__turns_count += 1

    def verify_move(self,action: FanoronaAction) -> str:
        if action.get_difference_x() == action.get_difference_x() and action.get_difference_y() < 0:
            return FanoronaState.DIAGONAL_DOWN
        if action.get_difference_x() == action.get_difference_x() and action.get_difference_y() > 0:
            return FanoronaState.DIAGONAL_UP
        if action.get_difference_x() == 0 and action.get_difference_y() < 0:
            return FanoronaState.HORIZONTAL_RIGHT
        if action.get_difference_x() == 0 and action.get_difference_y() > 0:
            return FanoronaState.HORIZONTAL_LEFT
        if action.get_difference_x() < 0 and action.get_difference_y() == 0:
            return FanoronaState.VERTICAL_DOWN
        if action.get_difference_x() > 0 and action.get_difference_y() == 0:
            return FanoronaState.VERTICAL_UP
        return FanoronaState.INVALID_MOVE


    def __display_cell(self, row, col):
        print({
                  0: 'W',
                  1: 'B',
                  FanoronaState.EMPTY_CELL: ' '
              }[self.__grid[row][col]], end="")

    def __display_numbers(self):
        for col in range(0, self.__num_cols):
            if col < 10:
                print(' ', end="")
            print(col, end="")
        print("")

    def __display_separator(self):
        for col in range(0, self.__num_cols):
            print("--", end="")
        print("-")

    def display(self):
        self.__display_numbers()
        self.__display_separator()

        for row in range(0, self.__num_rows):
            print('|', end="")
            for col in range(0, self.__num_cols):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
            self.__display_separator()

        self.__display_numbers()
        print("")

    def __is_full(self):
        return False

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = FanoronaState()
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        cloned_state.__last_move_p0 = self.__last_move_p0
        cloned_state.__last_move_p1 = self.__last_move_p1
        cloned_state.__grid = self.__grid
        return cloned_state

    def get_result(self, pos) -> Optional[FanoronaResult]:
        if self.__has_winner:
            return FanoronaResult.LOOSE if pos == self.__acting_player else FanoronaResult.WIN
        if self.__is_full():
            return FanoronaResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda initial_x,final_x,initial_y,final_y: FanoronaAction(initial_x,initial_y,final_x,final_y),
                range(0, self.get_num_cols()))
        ))

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
