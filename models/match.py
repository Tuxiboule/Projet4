"""define a match"""
from dataclasses import dataclass

from models.player import Player


@dataclass
class Match():
    player_1: Player
    player_2: Player
    result: Player
