from random import randint

from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState
from games.state import State


class RandomFanoronaPlayer(FanoronaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: FanoronaState):
        if state.get_last_piece_pos_actual() is not None:
            initial_x, initial_y = state.get_last_piece_pos_actual()
            return FanoronaAction(initial_x,initial_y,randint(0, state.get_num_rows() - 1), randint(0, state.get_num_cols() -1))
        return FanoronaAction(randint(0, state.get_num_rows() -1 ), randint(0, state.get_num_cols() -1),
                              randint(0, state.get_num_rows() -1), randint(0, state.get_num_cols() -1))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
