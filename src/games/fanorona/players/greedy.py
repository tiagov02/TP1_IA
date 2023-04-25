from random import choice
from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState
from games.state import State


class GreedyFanoronaPlayer(FanoronaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: FanoronaState):
        grid = state.get_grid()

        selected_col = None
        max_count = 0
        last_piece_pos = state.get_last_piece_pos_actual()

        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                return # Retorna a ação correspondente

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
