"""define a match"""
from dataclasses import dataclass

from models.player import Player


@dataclass
class Match():
    player_1: Player
    player_2: Player
    result: Player

    def set_result(self, player):
        """_summary_
        set result of a match
        Args:
            player (player) or (str) or (None): Player if a player won, str if draw, None is not informed
        """
        self.result = player
