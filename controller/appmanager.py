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
from views.helpers import validate_input


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
                current_tournament_name = display.resume_tournament_menu(tournament_manager.load_tournaments())
                current_tournament = tournament_manager.resume_tournament(current_tournament_name)
        # report menu
        elif main_menu == "3":
            report_menu = display.report_menu()
            # report players
            if report_menu == "1":
                report.player_list(player_manager.load_players())
            # report tournaments
            elif report_menu == "2":
                report.tournament_list(tournament_manager.load_tournaments())
            # report specific tournament details
            elif report_menu == "3":
                menu_choice = display.tournament_details(tournament_manager.load_tournaments())
                for tournament in tournament_manager.load_tournaments():
                    if menu_choice == tournament["name"]:
                        tournament = tournament_manager.convert_tournament_dict_to_class(tournament)
                        report.tournament_details(tournament)
        # tournament runs
        if current_tournament is not None:
            iteration_counter = current_tournament.current_round.round_number
            while iteration_counter < current_tournament.num_rounds:
                iteration_counter += 1
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
        first_name = validate_input("Prénom ? ", r"^[A-Za-zéèêëàâçîïôûùüÿñÉÈÊËÀÂÇÎÏÔÛÙÜŸÑ\s'\-]+$")
        last_name = validate_input("Nom de famille ? ", r"^[A-Za-zéèêëàâçîïôûùüÿñÉÈÊËÀÂÇÎÏÔÛÙÜŸÑ\s'\-]+$")
        birth_date = validate_input("Date de naissance ? Format DD/MM/YY : ",
                                    r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{2}$")
        national_chess_id = validate_input("national_chess_id ? Format AA12345 : ", r"^[A-Z]{2}\d{5}$")
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
            print(f"Pas de second joueur appairé avec {match.player_1.last_name} {match.player_1.first_name} | "
                  "Victoire par défaut 'Bye'"
                  f"| Erreur : {e}"
                  )

        try:
            match.result = Player(**match.result)
        except Exception as e:
            print(f"Pas de resultat renseigné pour le match {match.player_1.last_name} {match.player_1.first_name} VS "
                  f"{match.player_2.last_name} {match.player_2.first_name}"
                  f"| Erreur : {e}"
                  )
        return match
