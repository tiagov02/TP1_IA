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
    VERTICAL_DOWN = "vertical_down"
    VERTICAL_UP = "vertical_up"
    DIAGONAL_DOWN_RIGHT = "diagonal_down_right"
    DIAGONAL_DOWN_LEFT = "diagonal_down_left"
    DIAGONAL_UP_RIGHT = "diagonal_up_right"
    DIAGONAL_UP_LEFT = "diagonal_up_left"
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
                       [FanoronaState.WHITE_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.WHITE_CELL for _i in range(self.__num_cols)],
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

    def __check_winner(self):
        return True if self.get_opposite_cards() == 0 else False


    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: FanoronaAction) -> bool:
        move = self.verify_move(action).split("_")[0]
        if action.get_initial_x() > self.__num_rows  or action.get_initial_y() > self.__num_cols  \
            or action.get_final_x() > self.__num_rows or action.get_final_y() > self.__num_cols:
            return False
        if action.get_initial_x() < 0 or action.get_initial_y() < 0 or action.get_final_x() < 0 or action.get_final_y() < 0:
            return False
        if self.__grid[action.get_initial_x()][action.get_initial_y()] != self.__acting_player:
            return False
        if self.__grid[action.get_final_x()][action.get_final_y()] != FanoronaState.EMPTY_CELL :
            return False
        if move == FanoronaState.INVALID_MOVE:
            return False

        if self.__acting_player == 0 and self.__last_move_p0 is not None:
            if self.__last_move_p0 != move:
                return False
        if self.__acting_player == 1 and self.__last_move_p1 is not None:
            if self.__last_move_p1 != move:
                return False


        '''
        if self.last_piece_pos is not None and self.last_piece_pos != [action.get_final_x(), action.get_final_y()]:
            print()
            return False
        '''

        return True

    def get_last_piece_pos_actual(self):
        return self.last_piece_pos

    def get_num_player_cards(self):
        cont = 0
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] == self.__acting_player:
                    cont += 1
        return cont

    def get_opposite_cards(self):
        cont = 0
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] != self.__acting_player and self.__grid[row][col] != FanoronaState.EMPTY_CELL:
                    cont += 1
        return cont

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
            self.__last_move_p0 = move.split("_")[0]
        else:
            self.__last_move_p1 = move.split("_")[0]

       #move diag
        if move == FanoronaState.DIAGONAL_UP_LEFT or move == FanoronaState.DIAGONAL_DOWN_RIGHT:
            number_blanks = 0
            row = final_x
            col = final_y
            while True:
                row += 1
                col += 1
                if row > self.__num_rows - 1:
                    break
                if col > self.__num_cols - 1:
                    break
                if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                    if row + 1 < self.__num_rows and col + 1 < self.__num_cols :
                        if self.__grid[row + 1][col + 1] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[row + 1][col + 1] == self.__acting_player:
                            break
                if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                    col] != FanoronaState.EMPTY_CELL:
                    draw_pieces_down += 1
                    if row + 1 < self.__num_rows and col + 1 < self.__num_cols :
                        if self.__grid[row + 1][col + 1] == FanoronaState.EMPTY_CELL or self.__grid[row +1][
                            col +1] == self.__acting_player:
                            break

            row = final_x
            col = final_y
            number_blanks = 0
            while True:
                row -= 1
                col -= 1
                if row < 0:
                    break
                if col < 0:
                    break
                if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                    if row - 1 >= 0 and col - 1 >= 0:
                        if self.__grid[row - 1][col -1] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[row - 1][col - 1] == self.__acting_player:
                            break
                if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                    col] != FanoronaState.EMPTY_CELL:
                    draw_pieces_up += 1
                    if row - 1 >= 0 and col - 1 >= 0:
                        if self.__grid[row - 1][col - 1] == FanoronaState.EMPTY_CELL or self.__grid[row - 1][
                            col - 1] == self.__acting_player:
                            break

            if draw_pieces_down >= draw_pieces_up:
                row = final_x
                col = final_y
                number_blanks = 0
                while True:
                    row += 1
                    col += 1
                    if row >= self.__num_rows - 1:
                        break
                    if col >= self.__num_cols - 1:
                        break
                    if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                        if row + 1 < self.__num_rows and col + 1 < self.__num_cols:
                            if self.__grid[row + 1][col + 1] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[row + 1][col + 1] == self.__acting_player:
                                break
                    if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                        col] != FanoronaState.EMPTY_CELL:
                        self.__grid[row][col] = FanoronaState.EMPTY_CELL
                        if row + 1 < self.__num_rows and col + 1 < self.__num_cols:
                            if self.__grid[row + 1][col + 1] == FanoronaState.EMPTY_CELL or self.__grid[row + 1][
                                col + 1] == self.__acting_player:
                                break

            if draw_pieces_down < draw_pieces_up:
                row = final_x
                col = final_y
                number_blanks = 0
                while True:
                    row -= 1
                    col -= 1
                    if row < 0:
                        break
                    if col < 0:
                        break
                    if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                        if row - 1 >= 0 and col - 1 >= 0:
                            if self.__grid[row - 1][col - 1] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[row - 1][col - 1] == self.__acting_player:
                                break
                    if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                        col] != FanoronaState.EMPTY_CELL:
                        self.__grid[row][col] = FanoronaState.EMPTY_CELL
                        if row - 1 >= 0 and col - 1 >= 0:
                            if self.__grid[row - 1][col - 1] == FanoronaState.EMPTY_CELL or self.__grid[row - 1][
                                col - 1] == self.__acting_player:
                                break
        #endmove
        if move == FanoronaState.DIAGONAL_UP_RIGHT or move == FanoronaState.DIAGONAL_DOWN_LEFT:
            number_blanks = 0
            row = final_x
            col = final_y
            while True:
                row += 1
                col -= 1
                if row > self.__num_rows - 1:
                    break
                if col < 0:
                    break
                if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                    if row + 1 < self.__num_rows and col - 1 >= 0:
                        if self.__grid[row + 1][col - 1] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[row + 1][col - 1] == self.__acting_player:
                            break
                if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                    col] != FanoronaState.EMPTY_CELL:
                    draw_pieces_down += 1
                    if row + 1 < self.__num_rows and col - 1 >= 0:
                        if self.__grid[row + 1][col - 1] == FanoronaState.EMPTY_CELL or self.__grid[row + 1][
                            col - 1] == self.__acting_player:
                            break
            number_blanks = 0
            row = final_x
            col = final_y
            while True:
                row -= 1
                col += 1
                if row < 0:
                    break
                if col > self.__num_cols - 1:
                    break
                if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                    if row - 1 >= 0 and col + 1 < self.__num_cols:
                        if self.__grid[row - 1][col + 1] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[row - 1][col + 1] == self.__acting_player:
                            break
                if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                    col] != FanoronaState.EMPTY_CELL:
                    draw_pieces_up += 1
                    if row - 1 >= 0 and col + 1 < self.__num_cols:
                        if self.__grid[row - 1][col + 1] == FanoronaState.EMPTY_CELL or self.__grid[row - 1][
                            col + 1] == self.__acting_player:
                            break
            if draw_pieces_down >= draw_pieces_up:
                number_blanks = 0
                row = final_x
                col = final_y
                while True:
                    row += 1
                    col -= 1
                    if row > self.__num_rows - 1:
                        break
                    if col < 0:
                        break
                    if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                        if row + 1 < self.__num_rows and col - 1 >= 0:
                            if self.__grid[row + 1][row - 1] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[row + 1][row - 1] == self.__acting_player:
                                break
                    if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                        col] != FanoronaState.EMPTY_CELL:
                        self.__grid[row][col] = FanoronaState.EMPTY_CELL
                        if row + 1 < self.__num_rows and col - 1 >= 0:
                            if self.__grid[row + 1][col - 1] == FanoronaState.EMPTY_CELL or self.__grid[row + 1][
                                col - 1] == self.__acting_player:
                                break
            if draw_pieces_down < draw_pieces_up:
                number_blanks = 0
                row = final_x
                col = final_y
                while True:
                    row -= 1
                    col += 1
                    if row < 0:
                        break
                    if col > self.__num_cols - 1:
                        break
                    if self.__grid[row][col] == FanoronaState.EMPTY_CELL:
                        if row - 1 >= 0 and col + 1 < self.__num_cols:
                            if self.__grid[row - 1][col + 1] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[row - 1][col + 1] == self.__acting_player:
                                break
                    if self.__grid[row][col] != self.__acting_player and self.__grid[row][
                        col] != FanoronaState.EMPTY_CELL:
                        self.__grid[row][col] = FanoronaState.EMPTY_CELL
                        if row - 1 >= 0 and col + 1 < self.__num_cols:
                            if self.__grid[row - 1][col + 1] == FanoronaState.EMPTY_CELL or self.__grid[row - 1][
                                col + 1] == self.__acting_player:
                                break


        #verifications if the move is vertical
        if move == FanoronaState.VERTICAL_UP or move == FanoronaState.VERTICAL_DOWN:
            for i in range(initial_x + 1, self.__num_rows):
                if self.__grid[i][final_y] == self.__acting_player:
                    break
                if self.__grid[i][final_y] == FanoronaState.EMPTY_CELL:
                    if i + 1 < self.__num_rows:
                        if self.__grid[i + 1][final_y] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[i + 1][final_y] == self.__acting_player:
                            break
                if self.__grid[i][final_y] != self.__acting_player and self.__grid[i][final_y] != FanoronaState.EMPTY_CELL:
                    draw_pieces_down += 1
                    if i + 1 < self.__num_rows:
                        if self.__grid[i + 1][final_y] == FanoronaState.EMPTY_CELL or self.__grid[i + 1][final_y] == self.__acting_player:
                            break

            for i in range(initial_x - 1,-1,-1):
                if self.__grid[i][final_y] == self.__acting_player:
                    break
                if self.__grid[i][final_y] == FanoronaState.EMPTY_CELL:
                    if i - 1 >= 0:
                        if self.__grid[i - 1][final_y] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[i - 1][final_y] == self.__acting_player:
                            break
                if self.__grid[i][final_y] != self.__acting_player and self.__grid[i][final_y] != FanoronaState.EMPTY_CELL:
                    draw_pieces_up += 1
                    if i - 1 >= 0:
                        if self.__grid[i - 1][final_y] == FanoronaState.EMPTY_CELL or self.__grid[i - 1][final_y] == self.__acting_player:
                            break
            if draw_pieces_up >= draw_pieces_down:
                for i in range(initial_x - 1, -1, -1):
                    if self.__grid[i][final_y] == self.__acting_player:
                        break
                    if self.__grid[i][final_y] == FanoronaState.EMPTY_CELL:
                        if i - 1 >= 0:
                            if self.__grid[i - 1][final_y] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[i - 1][final_y] == self.__acting_player:
                                break
                    if self.__grid[i][final_y] != self.__acting_player and self.__grid[i][final_y] != FanoronaState.EMPTY_CELL:
                        self.__grid[i][final_y] = FanoronaState.EMPTY_CELL
                        if i + 1 >= 0:
                            if self.__grid[i - 1][final_y] == FanoronaState.EMPTY_CELL or self.__grid[i - 1][final_y] == self.__acting_player:
                                break

            if draw_pieces_up < draw_pieces_down:
                for i in range(initial_x + 1, self.__num_rows):
                    if self.__grid[i][final_y] == self.__acting_player:
                        break
                    if self.__grid[i][final_y] == FanoronaState.EMPTY_CELL:
                        if i + 1 < self.__num_rows:
                            if self.__grid[i + 1][final_y] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[i + 1][final_y] == self.__acting_player:
                                break
                    if self.__grid[i][final_y] != self.__acting_player and self.__grid[i][
                        final_y] != FanoronaState.EMPTY_CELL:
                        self.__grid[i][final_y] = FanoronaState.EMPTY_CELL
                        if i + 1 < self.__num_rows:
                            if self.__grid[i + 1][final_y] == FanoronaState.EMPTY_CELL or self.__grid[i + 1][
                                final_y] == self.__acting_player:
                                break



        #verifications if the move is horizontal
        if move == FanoronaState.HORIZONTAL_LEFT or move == FanoronaState.HORIZONTAL_RIGHT:

            for i in range(initial_y + 1, self.__num_cols):
                if self.__grid[final_x][i] == self.__acting_player:
                    break
                if self.__grid[final_x][i] == FanoronaState.EMPTY_CELL:
                    if i + 1 < self.__num_cols:
                        if self.__grid[final_x][i + 1] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[final_x][i + 1] == self.__acting_player:
                            break
                if self.__grid[final_x][i] != self.__acting_player and self.__grid[final_x][i] != FanoronaState.EMPTY_CELL:
                    draw_pieces_right += 1
                    if i + 1 < self.__num_cols:
                        if self.__grid[final_x][i + 1] == FanoronaState.EMPTY_CELL or self.__grid[final_x][i + 1] == self.__acting_player:
                            break

            for i in range(initial_y -1 , -1, -1):
                if self.__grid[final_x][i] == self.__acting_player:
                    break
                if self.__grid[final_x][i] == FanoronaState.EMPTY_CELL:
                    if i - 1 >= 0:
                        if self.__grid[final_x][i - 1] == FanoronaState.EMPTY_CELL:
                            continue
                        if self.__grid[final_x][i - 1] == self.__acting_player:
                            break
                if self.__grid[final_x][i] != self.__acting_player and self.__grid[final_x][i] != FanoronaState.EMPTY_CELL:
                    draw_pieces_left += 1
                    if i - 1 >= 0:
                        if self.__grid[final_x][i - 1] == FanoronaState.EMPTY_CELL or self.__grid[final_x][i - 1] == self.__acting_player:
                            break


            if draw_pieces_right >= draw_pieces_left :
                for i in range(initial_y + 1, self.__num_cols):
                    if self.__grid[final_x][i] == self.__acting_player:
                        break
                    if self.__grid[final_x][i] == FanoronaState.EMPTY_CELL:
                        if i + 1 < self.__num_cols:
                            if self.__grid[final_x][i + 1] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[final_x][i + 1] == self.__acting_player:
                                break
                    if self.__grid[final_x][i] != self.__acting_player and self.__grid[final_x][i] != FanoronaState.EMPTY_CELL:
                        self.__grid[final_x][i] = FanoronaState.EMPTY_CELL
                        if i + 1 < self.__num_cols:
                            if self.__grid[final_x][i + 1] == FanoronaState.EMPTY_CELL or self.__grid[final_x][i + 1] == self.__acting_player:
                                break
            if draw_pieces_right < draw_pieces_left:
                for i in range(initial_y - 1, -1, -1):
                    if self.__grid[final_x][i] == self.__acting_player:
                        break
                    if self.__grid[final_x][i] == FanoronaState.EMPTY_CELL:
                        if i - 1 >= 0:
                            if self.__grid[final_x][i - 1] == FanoronaState.EMPTY_CELL:
                                continue
                            if self.__grid[final_x][i - 1] == self.__acting_player:
                                break
                    if self.__grid[final_x][i] != self.__acting_player and self.__grid[final_x][
                        i] != FanoronaState.EMPTY_CELL:
                        self.__grid[final_x][i] = FanoronaState.EMPTY_CELL
                        if i - 1 >= 0:
                            if self.__grid[final_x][i - 1] == FanoronaState.EMPTY_CELL or self.__grid[final_x][i - 1] == self.__acting_player:
                                break

        self.last_piece_pos = [final_x,final_y]
        # switch to next player
        #verify if the player eat pieces if true does not change the player
        if draw_pieces_up == 0 and draw_pieces_down == 0 and draw_pieces_left == 0 and draw_pieces_right == 0:
            self.__acting_player = FanoronaState.BLACK_CELL if self.__acting_player == FanoronaState.WHITE_CELL else FanoronaState.WHITE_CELL
            self.last_piece_pos = None
            self.__last_move_p1 = None
            self.__last_move_p0 = None

        elif not self.have_possible_actions():
            self.__acting_player = FanoronaState.BLACK_CELL if self.__acting_player == FanoronaState.WHITE_CELL else FanoronaState.WHITE_CELL
            self.last_piece_pos = None
            self.__last_move_p1 = None
            self.__last_move_p0 = None

        # moves the piece
        self.__grid[final_x][final_y] = self.__grid[initial_x][initial_y]
        self.__grid[initial_x][initial_y] = FanoronaState.EMPTY_CELL

        # determine if there is a winner
        self.__has_winner = self.__check_winner()

        self.__turns_count += 1

    def get_player_positions(self):
        my_pos = []
        for row in range(0, self.get_num_rows()):
            for col in range(self.get_num_cols()):
                if self.get_grid()[row][col] == self.get_acting_player():
                    my_pos.append([row,col])
        return my_pos

    def get_empty_pos(self):
        empty_pos = []
        for row in range(0, self.get_num_rows()):
            for col in range(0, self.get_num_cols()):
                if self.get_grid()[row][col] == FanoronaState.EMPTY_CELL:
                    empty_pos.append([row,col])
        return empty_pos

    def have_possible_actions(self) -> bool:
        empty_pos = self.get_empty_pos()
        initial_x, initial_y = self.get_last_piece_pos_actual() or (None, None)

        for init_pos in self.get_player_positions():
            if initial_x is None or init_pos == [initial_x, initial_y]:
                initial_x, initial_y = init_pos
                for final_pos in empty_pos:
                    final_x, final_y = final_pos
                    if self.validate_action(FanoronaAction(initial_x, initial_y, final_x, final_y)):
                        return True
        return False

    def verify_move(self,action: FanoronaAction) -> str:
        if action.get_difference_x() == action.get_difference_y() and action.get_difference_y() > 0:
            return FanoronaState.DIAGONAL_UP_LEFT
        if action.get_difference_x() == (-1 * action.get_difference_y()) and action.get_difference_x() < 0:
            return FanoronaState.DIAGONAL_DOWN_LEFT
        if action.get_difference_x() == action.get_difference_y() and action.get_difference_y() < 0:
            return FanoronaState.DIAGONAL_DOWN_RIGHT
        if action.get_difference_x() == (-1 * action.get_difference_y()) and action.get_difference_y() < 0:
            return FanoronaState.DIAGONAL_UP_RIGHT
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
            print(f"\t{row}")
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
        cloned_state.last_piece_pos = self.last_piece_pos
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
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
