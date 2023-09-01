"""manages everything displayed on screen"""
from views.helpers import give_date


class Display():

    def main_menu(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        menu_choice = input("Choisir la fonction : \n1. Gérer les tournois\n2. Ajouter un joueur\n"
                            "3. Afficher des rapports \n")
        return menu_choice

    def tournament_menu(self):
        menu_choice = input("Choisir la fonction : \n1. Lancer un nouveau tournoi\n2. Reprendre un tournoi existant\n")
        return menu_choice

    def resume_tournament_menu(self):
        menu_choice = input("Renseigner le nom du tournoi à reprendre :")
        return menu_choice

    def ask_for_match_number(self):
        menu_choice = input("De quel match voulez vous renseigner le resultat ?\n")
        return menu_choice

    def ask_for_result(self, match_number, match_list):
        match = match_list[match_number]
        temp = int(input("Qui a gagné entre : \n 1. "
                         f"{match.player_1} \net "
                         f"\n 2. {match.player_2} ?\n"
                         " 3. Match nul \n"))
        if temp == 1:
            match.result = match_list[match_number].player_1
            match_list[match_number].player_1.point += 1
        elif temp == 2:
            match.result = match_list[match_number].player_2
            match_list[match_number].player_2.point += 1
        elif temp == 3:
            match.result = "Match nul"
            match_list[match_number].player_1.point += 0.5
            match_list[match_number].player_2.point += 0.5
        return match_list

    def match_list(self, round):
        match_list_str = []
        match_number = 0
        for match in round.match_list:
            match_number += 1
            if match.player_2 is None:
                match = (f"{match_number}. {match.player_1.first_name} {match.player_1.last_name} passe")
            else:
                match = (f"{match_number}. {match.player_1.first_name} {match.player_1.last_name} "
                         "contre "
                         f"{match.player_2.first_name} {match.player_2.last_name}"
                         f"\nGagnant : {match.result['first_name']} {match.result['last_name']}"
                         )
                match_list_str.append(match)
        return match_list_str

    def current_round(self, tournament):
        print(f"ROUND : {tournament.current_round.round_number}")
        for display_match in self.match_list(tournament.current_round):
            print(display_match)
        match_to_complete = self.ask_for_match_number()
        tournament.current_round.match_list = (
            self.ask_for_result((int(match_to_complete) - 1),
                                tournament.current_round.match_list)
                                                        )

    def next_round(self, tournament):
        tournament.current_round.end_time = give_date()
        print("Tous les matchs renseignés, passage au round suivant\n CLASSEMENT")
        tournament = tournament.next_round()
        n = 0
        for player in tournament.players:
            n += 1
            print(f"{n}. {player.first_name} {player.last_name} : {player.point} points")
        return tournament

    def tournament_end(self, tournament):
        tournament.end_date = give_date()
        print("Tournoi terminé, retour à l'accueil")

    def report_menu(self):
        menu_choice = input("1. Liste des joueurs par ordre alphabétique\n"
                            "2. Liste de tous les tournois\n"
                            "3. Détails d'un tournoi\n"
                            )
        return menu_choice

    def tournament_details(self):
        menu_choice = input("Saisir le nom du tournoi : ")
        return menu_choice


class Report():
    def player_list(self, players):
        for player in players:
            print(player.last_name, player.first_name)

    def tournament_list(self, tournaments):
        for tournament in tournaments:
            print(tournament["name"], tournament["location"], tournament["start_date"], tournament["description"])

    def tournament_details(self, tournament):  # name / date, players, rounds & matches

        display = Display()
        print(f"Nom du tournoi : {tournament.name}\n"
              f"Date de début du tournoi : {tournament.start_date}\n"
              "\nListe des participants :"
              )
        for player in tournament.players:
            print(player.last_name, player.first_name)

        for round in tournament.round_list:
            print(f"\nRound n° : {round.round_number}, début : {round.begin_time}")
            for match in display.match_list(round):
                print(match)
