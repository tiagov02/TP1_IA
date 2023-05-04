from games.connect4.players.greedy import GreedyConnect4Player
from games.connect4.players.minimax import MinimaxConnect4Player
from games.connect4.players.random import RandomConnect4Player
from games.connect4.simulator import Connect4Simulator
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


    num_iterations = 1000

    c4_simulations = [
        # uncomment to play as human
        #{
        #    "name": "Connect4 - Human VS Random",
        #    "player1": HumanConnect4Player("Human"),
        #    "player2": RandomConnect4Player("Random")
        #},
        {
            "name": "Connect4 - Random VS Random",
            "player1": RandomConnect4Player("Random 1"),
            "player2": RandomConnect4Player("Random 2")
        },
        {
            "name": "Connect4 - Greedy VS Random",
            "player1": GreedyConnect4Player("Greedy"),
            "player2": RandomConnect4Player("Random")
        },
        {
            "name": "Minimax VS Random",
            "player1": MinimaxConnect4Player("Minimax"),
            "player2": RandomConnect4Player("Random")
        },
        {
            "name": "Minimax VS Greedy",
            "player1": MinimaxConnect4Player("Minimax"),
            "player2": GreedyConnect4Player("Greedy")
        }
    ]

    poker_simulations = [
        # uncomment to play as human
        #{
        #    "name": "Connect4 - Human VS Random",
        #    "player1": HumanKuhnPokerPlayer("Human"),
        #    "player2": RandomKuhnPokerPlayer("Random")
        #},
        {
            "name": "Kuhn Poker - Random VS Random",
            "player1": RandomKuhnPokerPlayer("Random 1"),
            "player2": RandomKuhnPokerPlayer("Random 2")
        },
        {
            "name": "Kuhn Poker - AlwaysBet VS Random",
            "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
            "player2": RandomKuhnPokerPlayer("Random")
        },
        {
            "name": "Kuhn Poker - AlwaysPass VS Random",
            "player1": AlwaysPassKuhnPokerPlayer("AlwaysPass"),
            "player2": RandomKuhnPokerPlayer("Random")
        },
        {
            "name": "Kuhn Poker - AlwaysBet VS AlwaysPass",
            "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
            "player2": AlwaysPassKuhnPokerPlayer("AlwaysPass")
        },
        {
            "name": "Kuhn Poker - AlwaysBet VS AlwaysBetKing",
            "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
            "player2": AlwaysBetKingKuhnPokerPlayer("AlwaysBetKing")
        },
        {
            "name": "Kuhn Poker - CFR VS Random",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": RandomKuhnPokerPlayer("Random")
        },
        {
            "name": "Kuhn Poker - CFR VS AlwaysPass",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": AlwaysPassKuhnPokerPlayer("AlwaysPass")
        },
        {
            "name": "Kuhn Poker - CFR VS AlwaysBet",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": AlwaysBetKuhnPokerPlayer("AlwaysBet")
        },
        {
            "name": "Kuhn Poker - CFR VS AlwaysBetKing",
            "player1": CFRKuhnPokerPlayer("CFR"),
            "player2": AlwaysBetKingKuhnPokerPlayer("AlwaysBetKing")
        }
    ]

    for sim in c4_simulations:
        run_simulation(sim["name"], Connect4Simulator(sim["player1"], sim["player2"]), num_iterations)

    for sim in poker_simulations:
        run_simulation(sim["name"], KuhnPokerSimulator(sim["player1"], sim["player2"]), num_iterations)

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
        print()
    elif option == 3:
        run_simulation("Fanorona",
                       FanoronaSimulator(
                           RandomFanoronaPlayer("2"),
                           OffensiveMinimaxFanoronaPlayer("1")
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
    run_simulation("Fanorona",
                   FanoronaSimulator(
                       OffensiveMinimaxFanoronaPlayer("1",of_heuristic),
                       OffensiveMinimaxFanoronaPlayer("2",df_heuristic),
                   ),
                   1)
#TODO : HEURISTIC OFFENSIVE
