"""define a player"""
from dataclasses import dataclass


@dataclass
class Player():
    first_name: str
    last_name: str
    birth_date: str
    national_chess_id: str
    point: float = 0
