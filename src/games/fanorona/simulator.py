from games.fanorona.player import FanoronaPlayer
from games.fanorona.state import FanoronaState
from games.game_simulator import GameSimulator


class FanoronaSimulator(GameSimulator):

    def __init__(self, player1: FanoronaPlayer, player2: FanoronaPlayer, num_rows: int = 6, num_cols: int = 7):
        super(FanoronaSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the fanorona grid
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols

    def init_game(self):
        return FanoronaState(self.__num_rows, self.__num_cols)

    def before_end_game(self, state: FanoronaState):
        # ignored for this simulator
        pass

    def end_game(self, state: FanoronaState):
        # ignored for this simulator
        pass
