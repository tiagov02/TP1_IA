from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState


class HumanFanoronaPlayer(FanoronaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: FanoronaState):
        state.display()
        last_piece_pos = state.get_last_piece_pos_actual()
        while True:
            # noinspection PyBroadException
            try:
                if last_piece_pos is None:
                    initial_x = int(input(f"Player {state.get_acting_player()}, choose the line of the piece that you"
                                          f"want to move: "))
                    initial_y = int(input("and the column: "))
                    final_x = int(input(f"and now the line that you want to move: "))
                    final_y = int(input("and a column: "))
                    return FanoronaAction(initial_x=initial_x,
                                          initial_y=initial_y,
                                          final_x=final_x,
                                          final_y=final_y)
                else:
                    initial_x,initial_y = last_piece_pos
                    print(f"Player {state.get_acting_player()}, choose the line of the piece that you"
                                          f"want to move: {initial_x}")
                    print(f"and the column: {initial_y}")
                    final_x = int(input(f"and now the line that you want to move: "))
                    final_y = int(input("and a column: "))
                    return FanoronaAction(initial_x=initial_x,
                                          initial_y=initial_y,
                                          final_x=final_x,
                                          final_y=final_y)
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: FanoronaState):
        # ignore
        pass

    def event_end_game(self, final_state: FanoronaState):
        # ignore
        pass
