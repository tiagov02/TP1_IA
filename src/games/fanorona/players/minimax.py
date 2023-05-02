import math

from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.result import FanoronaResult
from games.fanorona.state import FanoronaState
from games.state import State


class MinimaxFanoronaPlayer(FanoronaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_possible_actions(self, state: FanoronaState):
        possible_actions = []
        empty_pos = state.get_empty_pos()
        initial_x, initial_y = state.get_last_piece_pos_actual() or (None, None)

        for init_pos in state.get_player_positions():
            if initial_x is None or init_pos == [initial_x, initial_y]:
                initial_x, initial_y = init_pos
                for final_pos in empty_pos:
                    final_x, final_y = final_pos
                    if state.validate_action(FanoronaAction(initial_x, initial_y, final_x, final_y)):
                        possible_actions.append([initial_x, initial_y, final_x, final_y])

        return possible_actions

    def get_my_mobility(self, state: FanoronaState):
        return len(self.get_possible_actions(state))

    #TODO:
    def __heuristic(self, state: FanoronaState):
        """Because 45 is the maximum of blank spaces"""
        mobility = self.get_my_mobility(state) / 45
        percent_pieces = state.get_num_player_cards()/(state.get_num_player_cards()+ state.get_opposite_cards())
        return (0.7* percent_pieces) + (0.3 * mobility)

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
                FanoronaResult.LOOSE: 0 # heuristic between [0,1] not included
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
        state.display()
        return self.minimax(state, 5)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
