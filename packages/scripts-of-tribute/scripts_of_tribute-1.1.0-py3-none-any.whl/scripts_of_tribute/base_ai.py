from typing import List

from scripts_of_tribute.board import GameState, EndGameState
from scripts_of_tribute.enums import PatronId
from scripts_of_tribute.move import BasicMove

class BaseAI:
    def __init__(self, bot_name):
        self.bot_name = bot_name

    def pregame_prepare(self):
        pass

    def select_patron(self, available_patrons: List[PatronId]):
        raise NotImplementedError

    def play(self, game_state: GameState, possible_moves: List[BasicMove], remaining_time: int) -> BasicMove:
        raise NotImplementedError

    def game_end(self, end_game_state: EndGameState, final_state: GameState):
        pass
