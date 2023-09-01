"""define a round"""
from dataclasses import dataclass

from models.match import Match


@dataclass
class Round():
    round_number: int
    match_list: list[Match]
    begin_time: str
    end_time: str
