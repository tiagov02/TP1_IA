from games.fanorona.action import FanoronaAction
from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState


class HumanFanoronaPlayer(FanoronaPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: FanoronaState):
        state.display()
        while True:
            # noinspection PyBroadException
            try:
                return FanoronaAction(int(input(f"Player {state.get_acting_player()}, choose a column: ")))
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: FanoronaState):
        # ignore
        pass

    def event_end_game(self, final_state: FanoronaState):
        # ignore
        pass
