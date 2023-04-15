from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState
from games.game_simulator import GameSimulator


class FanoronaSimulator(GameSimulator):

    def __init__(self, player1: FanoronaPlayer, player2: FanoronaPlayer):
        super(FanoronaSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the fanorona grid
        """


    def init_game(self):
        return FanoronaState()

    def before_end_game(self, state: FanoronaState):
        # ignored for this simulator
        pass

    def end_game(self, state: FanoronaState):
        # ignored for this simulator
        pass
