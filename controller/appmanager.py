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
        """_summary_
        Main controller, manages the main loop
        """

        # initalise managers
        player_manager = PlayerManager()
        tournament_manager = TournamentManager()
        current_tournament = None

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

        if current_tournament is not None:
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

    def load_players(self):
        """_summary_
        load all players from .json file
        converts them to player class

        Returns:
            list[Player]: list of Class player
        """
        json_file_path = os.path.join("data", "tournaments", "players.json")
        with open(json_file_path, "r") as file:
            data = json.load(file)
            players = self.convert_players_dict_to_class(data["players"])
            return players

    def save_players(self, players_list):
        """_summary_
        save a list of class players into a .json file

        Args:
            players_list (list[player]): list of class' player
        """
        players_list = sorted(players_list, key=lambda player: (player.last_name, player.first_name))
        players_list = self.convert_player_class_to_dict(players_list)
        json_file_path = os.path.join("data", "tournaments", "players.json")
        with open(json_file_path, "w") as file:
            json.dump({"players": players_list}, file, indent=4)

    def add_player(self):
        """_summary_
        add a player into a .json file
        """
        first_name = input("Prénom ? ")
        last_name = input("Nom de famille ? ")
        birth_date = input("Date de naissance ? ")
        national_chess_id = input("national_chess_id ? ")
        new_player = Player(first_name, last_name, birth_date, national_chess_id)
        players_list = self.load_players()
        players_list.append(new_player)
        self.save_players(players_list)

    def convert_players_dict_to_class(self, players_dict):
        """_summary_
        convert a list of dictionary players to a liste of class players
        Args:
            players_dict (list[dict]): list of dictionary's player

        Returns:
            list[Player]: list of class' players
        """
        players = []
        for player in players_dict:
            player = Player(**player)
            players.append(player)
        return players

    def convert_player_class_to_dict(self, players):
        """_summary_
        converts a class to a dict
        Args:
            players (list[Player]): list of class' player

        Returns:
            list[dict]: list of dictionary's player
        """
        players_dict = []
        for player in players:
            player = asdict(player)
            players_dict.append(player)
        return players_dict


class TournamentManager():

    def load_tournaments(self):
        """_summary_
        Loads all tournaments from .json file
        Returns:
            list[dict]: list of dictionary's tournaments
        """
        json_file_path = os.path.join("data", "tournaments", "tournaments.json")
        with open(json_file_path, "r") as file:
            data = json.load(file)
            return data["tournaments"]

    def save_tournaments(self, tournament):
        """_summary_
        Saves a tournament in a .json file
        Args:
            tournament (Tournament): tournament to save
        """
        tournaments = self.load_tournaments()
        for existing_tournament in tournaments:
            if existing_tournament["name"] == tournament["name"]:
                existing_tournament.update(tournament)
                break

        json_file_path = os.path.join("data", "tournaments", "tournaments.json")
        with open(json_file_path, "w") as file:
            json.dump({"tournaments": tournaments}, file, indent=4)

    def start_new_tournament(self, players):
        """_summary_
        initalise a new tournament
        Args:
            players (list[Player]): list of class' player

        Returns:
            Tournament: a tournament class object
        """
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
        """_summary_
        add a tournament to a json file
        Args:
            tournament (dict): dictionary's tournament
        """
        tournaments = self.load_tournaments()
        tournaments.append(tournament)
        json_file_path = os.path.join("data", "tournaments", "tournaments.json")
        with open(json_file_path, "w") as file:
            json.dump({"tournaments": tournaments}, file, indent=4)

    def resume_tournament(self, resumed_tournament_name):
        """_summary_
        resume an existing tournament from his name
        Args:
            resumed_tournament_name (str): tournament's name

        Returns:
            Tournament: class' tournament
        """
        tournaments_list = self.load_tournaments()
        for tournament in tournaments_list:
            if resumed_tournament_name == tournament["name"]:
                tournament = self.convert_tournament_dict_to_class(tournament)
                if tournament.current_round.round_number <= tournament.num_rounds:
                    return tournament
                else:
                    print("Tournoi déjà terminé")

    def convert_tournament_dict_to_class(self, tournament):
        """_summary_
        converts a dictionary to a class' tournament
        Args:
            tournament (dict): dictionary's tournament

        Returns:
            Tournament: class' tournament
        """
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
        """_summary_
        convert a class' tournament to a dictionary's tournament
        Args:
            tournament (Tournament): class' tournament

        Returns:
            dict: dictionary's tournament
        """
        tournament = asdict(tournament)
        return tournament


class RoundManager():

    def convert_round_dict_to_class(self, round):
        """_summary_
        convert dictionary's round to class' round
        Args:
            round (dict): dictionary's round

        Returns:
            Round: class' round
        """
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
        """_summary_
        convert dictionary's match to a class
        Args:
            match (dict): dictionary's match

        Returns:
            Match: class' match
        """
        player_1 = Player(**match["player_1"])
        if match["player_2"] is not None:
            player_2 = Player(**match["player_2"])
        match = Match(**match)
        match.player_1 = player_1

        try:
            match.player_2 = player_2
        except Exception as e:
            print(e)

        try:
            match.result = Player(**match.result)
        except Exception as e:
            print(e)
        return match
