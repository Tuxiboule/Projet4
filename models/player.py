"""define a player"""
from dataclasses import dataclass


@dataclass
class Player():
    first_name: str
    last_name: str
    birth_date: str
    national_chess_id: str
    point: float = 0

    def addpoint(self, point):
        """_summary_
        add X point to a player
        Args:
            point (float): amount of point added to player
        """
        self.point += point
