import math

from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState
from games.state import State


class GreedyFanoronaPlayer(FanoronaPlayer):

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

    def get_action(self, state: FanoronaState):
        grid = state.get_grid()

        player = self.get_current_pos()
        opponent = 0 if player == 1 else 1

        selected_action = None
        empty_pos = self.get_empty_pos(state)
        no_cards = math.inf
        initial_x = None
        initial_y = None
        if state.get_last_piece_pos_actual() is not None:
            initial_x , initial_y = state.get_last_piece_pos_actual()

        if initial_x is not None and initial_y is not None:
            for pos in empty_pos:
                final_x, final_y = pos
                if state.validate_action(FanoronaAction(initial_x,initial_y,final_x,final_y)):
                    temp_state = state.clone()
                    temp_state.update(FanoronaAction(initial_x,initial_y,final_x,final_y))
                    if temp_state.count_cards(opponent) < no_cards:
                        no_cards = temp_state.get_opposite_cards()
                        selected_action = FanoronaAction(initial_x,initial_y,final_x,final_y)

        else:
            for init_pos in self.get_my_positions(state):
                initial_x, initial_y = init_pos
                for final_pos in empty_pos:
                    final_x, final_y = final_pos
                    if state.validate_action(FanoronaAction(initial_x, initial_y, final_x, final_y)):
                        temp_state = state.clone()
                        temp_state.update(FanoronaAction(initial_x, initial_y, final_x, final_y))
                        if temp_state.count_cards(opponent) < no_cards:
                            no_cards = temp_state.count_cards(opponent)
                            selected_action = FanoronaAction(initial_x, initial_y, final_x, final_y)

        if selected_action is None:
            raise Exception("There is no valid action")

        return selected_action



    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
