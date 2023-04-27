import math

from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.result import FanoronaResult
from games.fanorona.state import FanoronaState
from games.state import State


class MinimaxFanoronaPlayer(FanoronaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_empty_pos(self,state: FanoronaState):
        empty_pos = []
        for row in range(0, state.get_num_rows()):
            for col in range(0, state.get_num_cols()):
                if state.get_grid()[row][col] == FanoronaState.EMPTY_CELL:
                    empty_pos.append([row,col])
        return empty_pos

    def get_my_positions(self, state: FanoronaState):
        my_pos = []
        for row in range(0, state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if state.get_grid()[row][col] == state.get_acting_player():
                    my_pos.append([row,col])
        return my_pos

    def get_possible_actions(self, state: FanoronaState):
        possible_actions = []
        empty_pos = self.get_empty_pos(state)
        initial_x = None
        initial_y = None
        if state.get_last_piece_pos_actual() is not None:
            initial_x, initial_y = state.get_last_piece_pos_actual()

        if initial_x is not None and initial_y is not None:
            for pos in empty_pos:
                final_x, final_y = pos
                if state.validate_action(FanoronaAction(initial_x, initial_y, final_x, final_y)):
                    possible_actions.append([initial_x,initial_y,final_x,final_y])
        else:
            for init_pos in self.get_my_positions(state):
                initial_x, initial_y = init_pos
                for final_pos in empty_pos:
                    final_x, final_y = final_pos
                    if state.validate_action(FanoronaAction(initial_x, initial_y, final_x, final_y)):
                        possible_actions.append([initial_x,initial_y,final_x,final_y])
        return possible_actions



    def __heuristic(self, state: FanoronaState):
        grid = state.get_grid()
        longest = 0

        # check each line
        for row in range(0, state.get_num_rows()):
            seq = 0
            for col in range(0, state.get_num_cols()):
                if grid[row][col] == self.get_current_pos():
                    seq += 1
                else:
                    if seq > longest:
                        longest = seq
                    seq = 0

            if seq > longest:
                longest = seq

        # check each column
        for col in range(0, state.get_num_cols()):
            seq = 0
            for row in range(0, state.get_num_rows()):
                if grid[row][col] == self.get_current_pos():
                    seq += 1
                else:
                    if seq > longest:
                        longest = seq
                    seq = 0

            if seq > longest:
                longest = seq

        # check each upward diagonal
        for row in range(3, state.get_num_rows()):
            for col in range(0, state.get_num_cols() - 3):
                seq1 = (1 if grid[row][col] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 2][col + 2] == self.get_current_pos() else 0)

                seq2 = (1 if grid[row - 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 2][col + 2] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 3][col + 3] == self.get_current_pos() else 0)

                if seq1 > longest:
                    longest = seq1

                if seq2 > longest:
                    longest = seq2

        # check each downward diagonal
        for row in range(0, state.get_num_rows() - 3):
            for col in range(0, state.get_num_cols() - 3):
                seq1 = (1 if grid[row][col] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 2][col + 2] == self.get_current_pos() else 0)

                seq2 = (1 if grid[row + 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 2][col + 2] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 3][col + 3] == self.get_current_pos() else 0)

                if seq1 > longest:
                    longest = seq1

                if seq2 > longest:
                    longest = seq2

        return longest

    """Implementation of minimax search (recursive, with alpha/beta pruning) :param state: the state for which the 
    search should be made :param depth: maximum depth of the search :param alpha: to optimize the search :param beta: 
    to optimize the search :param is_initial_node: if true, the function will return the action with max ev, 
    otherwise it return the max ev (ev = expected value) """

    def minimax(self, state: FanoronaState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                FanoronaResult.WIN: 100,
                FanoronaResult.LOOSE: 0 #todo: heuristic between [0,100] not included
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            # very small integer
            value = -math.inf
            selected_action = None

            for action in state.get_possible_actions():
                pre_value = value
                value = max(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value > pre_value:
                    selected_action = action
                if value > beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        # if it is the opponent's turn
        else:
            value = math.inf
            for action in state.get_possible_actions():
                value = min(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value

    def get_action(self, state: FanoronaState):
        return self.minimax(state, 5)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
