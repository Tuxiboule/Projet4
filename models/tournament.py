"""define a tournament"""
import random
import copy
from dataclasses import dataclass

from models.player import Player
from models.round import Round
from models.match import Match
from views.helpers import give_date


@dataclass
class Tournament():
    name: str
    location: str
    start_date: str
    end_date: str
    num_rounds: int
    current_round: Round
    round_list: list[Round]
    players: list[Player]
    description: str

    def pairing(self):
        """_summary_
        pairs players depending on their ranking
        Returns:
            list(list(Player)): list of paired players
        """
        pairs = []
        if self.current_round.round_number == 1:
            random.shuffle(self.players)
            for i in range(0, len(self.players), 2):
                if i+1 < len(self.players):
                    pair = (self.players[i], self.players[i+1])
                    pairs.append(pair)

            if len(self.players) % 2 != 0:
                pairs.append((self.players[-1],))
        else:
            self.players = sorted(self.players, key=lambda player: player.point, reverse=True)
            for i in range(0, len(self.players), 2):
                if i+1 < len(self.players):
                    pair = (self.players[i], self.players[i+1])
                    pairs.append(pair)

            if len(self.players) % 2 != 0:
                pairs.append((self.players[-1],))
        return pairs

    def initialise_round(self):
        """_summary_
        initalise a new round
        Returns:
            Round: Round class
        """
        matches = self.initialise_matches()
        round = Round(1, matches, give_date(), None)
        self.current_round = round
        return self

    def initialise_matches(self):
        """
        Returns:
            list[Match]: list containing all matches
        """
        pairs = self.pairing()
        matches = []
        for pair in pairs:
            if len(pair) == 2:
                match = Match(pair[0], pair[1], None)
            else:
                match = Match(pair[0], None, None)
                match.result = pair[0]

            matches.append(match)
        return matches

    def next_round(self):
        """_summary_
        Pass to the next round
        Returns:
            Round: actualised round
        """
        self.round_list.append(copy.deepcopy(self.current_round))
        self.current_round.round_number += 1
        self.current_round.match_list = self.initialise_matches()
        return self
