from typing import Optional

from games.fanorona.action import FanoronaAction
from games.fanorona.result import FanoronaResult
from games.state import State


class FanoronaState(State):
    WHITE_CELL = 0
    BLACK_CELL = 1
    EMPTY_CELL = -1

    #MOOVES
    HORIZONTAL_RIGHT = "horizontal_right"
    HORIZONTAL_LEFT = "horizontal_left"
    VERTICAL_DOWN = "vertical_right"
    VERTICAL_UP = "vertical_up"
    DIAGONAL_DOWN = "diagonal_down"
    DIAGONAL_UP = "diagonal_up"

    def __init__(self, num_rows: int = 9, num_cols: int = 5):
        super().__init__()

        if num_rows < 4:
            raise Exception("the number of rows must be 5")
        if num_cols < 4:
            raise Exception("the number of cols must be 9")

        """
        the dimensions of the board
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols

        """
        the grid
        """
        #self.__grid = [[FanoronaState.WHITE_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]
        self.__grid = [[FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL,FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL,FanoronaState.EMPTY_CELL,FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL,FanoronaState.BLACK_CELL,FanoronaState.WHITE_CELL],
                       [FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       [FanoronaState.BLACK_CELL for _i in range(self.__num_cols)],
                       ]
        self.__last_moove_p0 = None
        self.__last_moove_p1 = None

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player
        """
        self.__acting_player = 0

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    def __check_winner(self, player):
        # check for 4 across
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row][col + 1] == player and \
                        self.__grid[row][col + 2] == player and \
                        self.__grid[row][col + 3] == player:
                    return True

        # check for 4 up and down
        for row in range(0, self.__num_rows - 3):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col] == player and \
                        self.__grid[row + 2][col] == player and \
                        self.__grid[row + 3][col] == player:
                    return True

        # check upward diagonal
        for row in range(3, self.__num_rows):
            for col in range(0, self.__num_cols - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row - 1][col + 1] == player and \
                        self.__grid[row - 2][col + 2] == player and \
                        self.__grid[row - 3][col + 3] == player:
                    return True

        # check downward diagonal
        for row in range(0, self.__num_rows - 3):
            for col in range(0, self.__num_cols - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col + 1] == player and \
                        self.__grid[row + 2][col + 2] == player and \
                        self.__grid[row + 3][col + 3] == player:
                    return True

        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: FanoronaAction) -> bool:
       return True

    def update(self, action: FanoronaAction):
        # x = action.get_x()
        # y = action.get_y()

        moove = self.verify_moove(action)
        if self.__acting_player == 0:
            self.__last_moove_p0 = moove
        else:
            self.__last_moove_p1 = moove

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def verify_moove(self,action: FanoronaAction) -> str:
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
        return self.__turns_count > (self.__num_cols * self.__num_rows)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = FanoronaState(self.__num_rows, self.__num_cols)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
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
                lambda pos: FanoronaAction(pos),
                range(0, self.get_num_cols()))
        ))

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
