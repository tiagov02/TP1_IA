from games.connect4.players.greedy import GreedyConnect4Player
from games.connect4.players.minimax import MinimaxConnect4Player
from games.connect4.players.random import RandomConnect4Player
from games.connect4.simulator import Connect4Simulator
from games.fanorona.players.defensive_minimax import DefensiveMinimaxFanoronaPlayer
from games.fanorona.players.greedy import GreedyFanoronaPlayer
from games.fanorona.players.human import HumanFanoronaPlayer
from games.fanorona.players.offensive_minimax import OffensiveMinimaxFanoronaPlayer
from games.fanorona.players.random import RandomFanoronaPlayer
from games.fanorona.simulator import FanoronaSimulator
from games.fanorona.state import FanoronaState
from games.game_simulator import GameSimulator
from games.poker.players.always_bet import AlwaysBetKuhnPokerPlayer
from games.poker.players.always_bet_king import AlwaysBetKingKuhnPokerPlayer
from games.poker.players.always_pass import AlwaysPassKuhnPokerPlayer
from games.poker.players.cfr import CFRKuhnPokerPlayer
from games.poker.players.random import RandomKuhnPokerPlayer
from games.poker.simulator import KuhnPokerSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def machineVSmachine():
    num_iterations = 5

    fanorona_simulations = [
        {
            "name": "Fanorona - Random VS Random",
            "player1": RandomFanoronaPlayer("Random 1"),
            "player2": RandomFanoronaPlayer("Random 2")
        },
        {
            "name": "Fanorona - Greedy VS Random",
            "player1": GreedyFanoronaPlayer("Greedy"),
            "player2": RandomFanoronaPlayer("Random")
        },
        {
            "name": "Fanorona - Greedy VS Greedy",
            "player1": GreedyFanoronaPlayer("Greedy 1"),
            "player2": RandomFanoronaPlayer("Greedy 2")
        },
        {
            "name": "Fanorona - Greedy VS Offensive Minimax",
            "player1":  OffensiveMinimaxFanoronaPlayer("Offensive Minimax"),
            "player2":  GreedyFanoronaPlayer("Greedy")
        },
        {
            "name": "Fanorona - Greedy VS Defensive Minimax",
            "player1": DefensiveMinimaxFanoronaPlayer("Defensive Minimax"),
            "player2": GreedyFanoronaPlayer("Greedy")
        },

        {
            "name": "Fanorona - Random VS Offensive Minimax",
            "player1": RandomFanoronaPlayer("Random"),
            "player2": DefensiveMinimaxFanoronaPlayer("Offensive Minimax")
        },
        {
            "name": "Fanorona - Random VS Defensive Minimax",
            "player1": RandomFanoronaPlayer("Random"),
            "player2": OffensiveMinimaxFanoronaPlayer("Offensive Minimax")
        }
    ]

    for sim in fanorona_simulations:
        run_simulation(sim["name"], FanoronaSimulator(sim["player1"],sim["player2"]),num_iterations)

def humanVsMachine():
    print("\tChoose your player:")
    print("1 - Greedy")
    print("2 - Random")
    print("3 - Defensive Minimax")
    print("4 - Offensive Minimax")
    option = int(input("Choose your option: "))
    if option == 1:
        run_simulation("Fanorona - You vs Greedy",
                       FanoronaSimulator(
                           HumanFanoronaPlayer("Human"),
                           GreedyFanoronaPlayer("Greedy")
                       ),
                       1)
    elif option == 2:
        run_simulation("Fanorona - You vs Random",
                       FanoronaSimulator(
                           HumanFanoronaPlayer("Human"),
                           RandomFanoronaPlayer("Random")
                       ),
                       1)
    elif option == 3:
        run_simulation("Fanorona - You vs Minimax",
                       FanoronaSimulator(
                           HumanFanoronaPlayer("Human"),
                           DefensiveMinimaxFanoronaPlayer("Minimax")
                       ),
                       1)
    elif option == 4:
        run_simulation("Fanorona - You vs Minimax",
                       FanoronaSimulator(
                           HumanFanoronaPlayer("Human"),
                           OffensiveMinimaxFanoronaPlayer("Minimax")
                       ),
                       1)

def main():
    num_iterations = 2
    print("ESTG IA Games Simulator")
    print("\t Choose your option")
    print("1 - machine vs machine")
    print("2 - you vs machine")
    print("3 - You vs Friend")
    option = int(input())

    if option == 1:
        machineVSmachine()
    elif option == 2:
        humanVsMachine()
    elif option == 3:
        run_simulation("Fanorona",
                       FanoronaSimulator(
                           HumanFanoronaPlayer("Player 1"),
                           HumanFanoronaPlayer("Player 2")
                       ),
                       num_iterations)

def of_heuristic(pl, state: FanoronaState):
    player = pl.get_current_pos()
    opponent = 0 if player == 1 else 1
    heuristic = 1 - state.count_cards(opponent) / 45
    return heuristic

def get_my_mobility(pl, state: FanoronaState):
    return len(pl.get_possible_actions(state))

#TODO:
def df_heuristic(pl, state: FanoronaState):
    player = pl.get_current_pos()
    opponent = 0 if player == 1 else 1
    """Because 45 is the maximum of blank spaces"""
    mobility = get_my_mobility(pl, state) / 45
    my_percent_occupation = state.count_cards(player) / 45
    opp_percent_occupation = state.count_cards(opponent) / 45
    heuristic = (0.7 * my_percent_occupation) + (0.3 * mobility)
    print(heuristic)
    return heuristic


if __name__ == "__main__":
    main()
    """
    greedy = GreedyFanoronaPlayer("2")
    run_simulation("Fanorona",
                   FanoronaSimulator(
                       greedy,
                       OffensiveMinimaxFanoronaPlayer("1")
                   ),
                   1)
                   """
#TODO : HEURISTIC OFFENSIVE
