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


    #TODO:
    def __heuristic(self, state: FanoronaState):
        return state.get_num_player_cards()/(state.get_num_player_cards()+ state.get_opposite_cards())

    """Implementation of minimax search (recursive, with alpha/beta pruning) :param state: the state for which the 
    search should be made :param depth: maximum depth of the search :param alpha: to optimize the search :param beta: 
    to optimize the search :param is_initial_node: if true, the function will return the action with max ev, 
    otherwise it return the max ev (ev = expected value) """

    def minimax(self, state: FanoronaState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                FanoronaResult.WIN: 1,
                FanoronaResult.LOOSE: 0 #todo: heuristic between [0,100] not included
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player --maximize the win
        if self.get_current_pos() == state.get_acting_player():
            # very small integer
            value = -math.inf
            selected_action = None

            for pos in self.get_possible_actions(state):
                pre_value = value
                initial_x, initial_y, final_x, final_y = pos
                value = max(value,
                            self.minimax(state.sim_play(FanoronaAction(initial_x,initial_y,final_x,final_y)), depth - 1, alpha, beta, False))
                if value > pre_value:
                    selected_action = FanoronaAction(initial_x,initial_y, final_x, final_y)
                if value > beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        # if it is the opponent's turn  --> minimize the loss
        else:
            value = math.inf
            for pos in self.get_possible_actions(state):
                initial_x, initial_y, final_x, final_y = pos
                value = min(value, self.minimax(state.sim_play(FanoronaAction(initial_x,initial_y,final_x,final_y)), depth - 1, alpha, beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value

    def get_action(self, state: FanoronaState):
        #state.display()
        return self.minimax(state, 5)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
