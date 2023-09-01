"""manages the application"""
import os
import json
from dataclasses import asdict

from models.tournament import Tournament
from models.player import Player
from models.match import Match
from models.round import Round
from views.display import Display
from views.display import Report
from views.helpers import give_date


class MainController:
    def run(self):

        # initalise managers
        player_manager = PlayerManager()
        tournament_manager = TournamentManager()

        # initialise display
        display = Display()
        main_menu = display.main_menu()

        # initialise report
        report = Report()

        # add a player
        if main_menu == "2":
            player_manager.add_player()

        # tournament menu
        elif main_menu == "1":
            # start a new tournament
            if display.tournament_menu() == "1":
                players = player_manager.load_players()
                current_tournament = tournament_manager.start_new_tournament(players)
                current_tournament = current_tournament.initialise_round()
                tournament_manager.save_tournaments(
                    tournament_manager.convert_tournament_class_to_dict(current_tournament)
                                                    )

            else:
                # resume existant tournament
                current_tournament_name = display.resume_tournament_menu()
                current_tournament = tournament_manager.resume_tournament(current_tournament_name)

        elif main_menu == "3":
            report_menu = display.report_menu()
            if report_menu == "1":
                report.player_list(player_manager.load_players())
            elif report_menu == "2":
                report.tournament_list(tournament_manager.load_tournaments())
            elif report_menu == "3":
                menu_choice = display.tournament_details()
                for tournament in tournament_manager.load_tournaments():
                    if menu_choice == tournament["name"]:
                        tournament = tournament_manager.convert_tournament_dict_to_class(tournament)
                        report.tournament_details(tournament)

        for n in range(current_tournament.num_rounds):
            for match in current_tournament.current_round.match_list:
                while match.result is None:
                    display.current_round(current_tournament)
                    tournament_manager.save_tournaments(
                        tournament_manager.convert_tournament_class_to_dict(current_tournament)
                                                        )
            current_tournament = display.next_round(current_tournament)
            tournament_manager.save_tournaments(
                tournament_manager.convert_tournament_class_to_dict(current_tournament)
                                                )
        display.tournament_end(current_tournament)


class PlayerManager():

    def __init__(self):
        # self.tournament = tournament
        pass

    def load_players(self):
        json_file_path = os.path.join("data", "tournaments", "players.json")
        with open(json_file_path, "r") as file:
            data = json.load(file)
            players = self.convert_players_dict_to_class(data["players"])
            return players

    def save_players(self, players_list):
        players_list = sorted(players_list, key=lambda player: (player.last_name, player.first_name))
        players_list = self.convert_player_class_to_dict(players_list)
        json_file_path = os.path.join("data", "tournaments", "players.json")
        with open(json_file_path, "w") as file:
            json.dump({"players": players_list}, file, indent=4)

    def add_player(self):
        first_name = input("Prénom ? ")
        last_name = input("Nom de famille ? ")
        birth_date = input("Date de naissance ? ")
        national_chess_id = input("national_chess_id ? ")
        new_player = Player(first_name, last_name, birth_date, national_chess_id)
        players_list = self.load_players()
        players_list.append(new_player)
        self.save_players(players_list)

    def convert_players_dict_to_class(self, players_dict):
        players = []
        for player in players_dict:
            player = Player(**player)
            players.append(player)
        return players

    def convert_player_class_to_dict(self, players):
        players_dict = []
        for player in players:
            player = asdict(player)
            players_dict.append(player)
        return players_dict


class TournamentManager():
    def load_tournaments(self):
        json_file_path = os.path.join("data", "tournaments", "tournaments.json")
        with open(json_file_path, "r") as file:
            data = json.load(file)
            return data["tournaments"]

    def save_tournaments(self, tournament):
        tournaments = self.load_tournaments()
        for existing_tournament in tournaments:
            if existing_tournament["name"] == tournament["name"]:
                existing_tournament.update(tournament)
                break

        json_file_path = os.path.join("data", "tournaments", "tournaments.json")
        with open(json_file_path, "w") as file:
            json.dump({"tournaments": tournaments}, file, indent=4)

    def start_new_tournament(self, players):
        name = input("Nom du tournoi ? ")
        location = input("Lieu du tournoi ? ")
        start_date = give_date()
        end_date = None
        num_rounds = 4
        current_round = Round(1, None, None, None)
        round_list = []
        description = input("Description du tournoi ")
        new_tournament = Tournament(name,
                                    location,
                                    start_date,
                                    end_date,
                                    num_rounds,
                                    current_round,
                                    round_list,
                                    players,
                                    description
                                    )
        new_tournament_dict = self.convert_tournament_class_to_dict(new_tournament)
        self.add_tournament(new_tournament_dict)
        return new_tournament

    def add_tournament(self, tournament):
        tournaments = self.load_tournaments()
        tournaments.append(tournament)
        json_file_path = os.path.join("data", "tournaments", "tournaments.json")
        with open(json_file_path, "w") as file:
            json.dump({"tournaments": tournaments}, file, indent=4)

    def resume_tournament(self, resumed_tournament_name):
        tournaments_list = self.load_tournaments()
        for tournament in tournaments_list:
            if resumed_tournament_name == tournament["name"]:
                return self.convert_tournament_dict_to_class(tournament)

    def convert_tournament_dict_to_class(self, tournament):
        players = []
        player_manager = PlayerManager()
        round_manager = RoundManager()
        tournament = Tournament(**tournament)
        players = player_manager.convert_players_dict_to_class(tournament.players)
        tournament.players = players
        current_round = round_manager.convert_round_dict_to_class(tournament.current_round)
        tournament.current_round = current_round
        class_round_list = []
        for round in tournament.round_list:
            round = round_manager.convert_round_dict_to_class(round)
            class_round_list.append(round)
        tournament.round_list = class_round_list
        return tournament

    def convert_tournament_class_to_dict(self, tournament):
        tournament = asdict(tournament)
        return tournament


class RoundManager():

    def convert_round_dict_to_class(self, round):
        match_manager = MatchManager()
        match_list = []
        round = Round(**round)
        for match in round.match_list:
            match = match_manager.convert_match_dict_to_class(match)
            match_list.append(match)
        round.match_list = match_list
        return round


class MatchManager():

    def convert_match_dict_to_class(self, match):
        player_1 = Player(**match["player_1"])
        if match["player_2"] is not None:
            player_2 = Player(**match["player_2"])
        match = Match(**match)
        match.player_1 = player_1
        try:
            match.player_2 = player_2
        except Exception as e:
            print(e)
        return match
