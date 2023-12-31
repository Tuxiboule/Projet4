"""manages everything displayed on screen"""
from views.helpers import give_date


class Display():

    def main_menu(self):
        """_summary_
        Main menu of the program
        Returns:
            str: choice in the menu
        """
        menu_choice = input("Choisir la fonction : \n1. Gérer les tournois\n2. Ajouter un joueur\n"
                            "3. Afficher des rapports \n")
        while menu_choice not in ("1", "2", "3"):
            print("Saisie éronée, veuillez renseigner une saisie valide")
            menu_choice = input("Choisir la fonction : \n1. Gérer les tournois\n2. Ajouter un joueur\n"
                                "3. Afficher des rapports \n")
        return menu_choice

    def tournament_menu(self):
        """_summary_
        Menu to handle tournaments
        Returns:
            str: choice in the menu
        """
        menu_choice = input("Choisir la fonction : \n1. "
                            "Lancer un nouveau tournoi\n2. Reprendre un tournoi existant\n"
                            )
        while menu_choice not in ("1", "2"):
            print("Saisie éronée, veuillez renseigner une saisie valide")
            menu_choice = input("Choisir la fonction : \n1. "
                                "Lancer un nouveau tournoi\n2. Reprendre un tournoi existant\n"
                                )
        return menu_choice

    def resume_tournament_menu(self, tournaments):
        """_summary_
        Menu to input wich tournament to resume
        Args:
            tournaments (list): List of tournament dictionaries

        Returns:
            str: name of chosen tournament
        """
        while True:
            menu_choice = input("Renseigner le nom du tournoi à reprendre :")
            for tournament in tournaments:
                if tournament["name"] == menu_choice:
                    return menu_choice
            print("Ce tournoi n'existe pas, veuillez renseigner un nom valide")

    def ask_for_match_number(self, current_round):
        """_summary_
        Menu to ask user wich match to complete
        Returns:
            str: choice in the menu
        """
        while True:
            menu_choice = input("De quel match voulez vous renseigner le resultat ?\n")
            if not (1 <= int(menu_choice) <= len(current_round.match_list)):
                print("Saisie éronée, veuillez renseigner une saisie valide")
            elif current_round.match_list[int(menu_choice) - 1].result is not None:
                print("Ce match a déjà un résultat enregistré.")
            else:
                return menu_choice

    def ask_for_result(self, match_number, match_list):
        """_summary_
        Menu to ask the result of a match
        Args:
            match_number (int): number of the match
            match_list (list[Match]): list of all matches

        Returns:
           list[str]:
        """
        match = match_list[match_number]
        menu_choice = int(input("Quel est le résultat du match : \n1. "
                                f"{match.player_1.last_name}, {match.player_1.first_name} \n"
                                f"2. {match.player_2.last_name}, {match.player_2.first_name} ?\n"
                                "3. Match nul \n"
                                )
                          )
        while menu_choice not in (1, 2, 3):
            print("Saisie éronée, veuillez renseigner une saisie valide")
            menu_choice = int(input("Qui a gagné entre : \n 1. "
                                    f"{match.player_1.last_name}, {match.player_1.first_name} \net "
                                    f"\n 2. {match.player_2.last_name}, {match.player_2.first_name} ?\n"
                                    " 3. Match nul \n"
                                    )
                              )
        # P1 won
        if menu_choice == 1:
            match.set_result(match_list[match_number].player_1)
            match_list[match_number].player_1.addpoint(1)
        # P2 Won
        elif menu_choice == 2:
            match.set_result(match_list[match_number].player_2)
            match_list[match_number].player_2.addpoint(1)
        # Draw
        elif menu_choice == 3:
            match.set_result("Match nul")
            match_list[match_number].player_1.addpoint(0.5)
            match_list[match_number].player_2.addpoint(0.5)

        return match_list

    def match_list(self, round):
        """_summary_
        Returns a list of matches ready to be displayed
        Args:
            round (Round): class' round

        Returns:
            list[str]: list of displayed matches
        """
        match_list_str = []
        match_number = 0
        for match in round.match_list:
            match_number += 1
            # Player have no oppenent
            if match.player_2 is None:
                match = (f"{match_number}. {match.player_1.first_name} {match.player_1.last_name} | Bye")
            # Match result is not known yet
            elif match.result is None:
                match = (f"{match_number}. {match.player_1.first_name} {match.player_1.last_name} "
                         "contre "
                         f"{match.player_2.first_name} {match.player_2.last_name}"
                         )
            # Match is draw
            elif match.result == "Match nul":
                match = (f"{match_number}. {match.player_1.first_name} {match.player_1.last_name} "
                         "contre "
                         f"{match.player_2.first_name} {match.player_2.last_name} "
                         "| Match nul"
                         )
            # Match winner is known and not draw
            else:
                match = (f"{match_number}. {match.player_1.first_name} {match.player_1.last_name} "
                         "contre "
                         f"{match.player_2.first_name} {match.player_2.last_name}"
                         f" | Gagnant : {match.result.first_name} {match.result.last_name}"
                         )
            match_list_str.append(match)
        return match_list_str

    def current_round(self, tournament):
        """_summary_
        Display the current round's match list
        Args:
            tournament (Tournament): class' tournament
        """
        print(f"ROUND : {tournament.current_round.round_number}")
        for display_match in self.match_list(tournament.current_round):
            print(display_match)
        match_to_complete = self.ask_for_match_number(tournament.current_round)
        tournament.current_round.match_list = (
            self.ask_for_result((int(match_to_complete) - 1),
                                tournament.current_round.match_list))

    def next_round(self, tournament):
        """_summary_
        Displays ranking at the end of a round
        Args:
            tournament (Tournament): class' tournament

        Returns:
            Tournament: class' tournament
        """
        tournament.current_round.end_time = give_date()
        print("Tous les matchs renseignés, passage au round suivant\n ----CLASSEMENT----")
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
        """_summary_
        Display menu for tournament reports
        Returns:
            str: choice in the menu
        """
        menu_choice = input("1. Liste des joueurs par ordre alphabétique\n"
                            "2. Liste de tous les tournois\n"
                            "3. Détails d'un tournoi\n"
                            )
        while menu_choice not in ("1", "2", "3"):
            print("Saisie éronée, veuillez renseigner une saisie valide")
            menu_choice = input("1. Liste des joueurs par ordre alphabétique\n"
                                "2. Liste de tous les tournois\n"
                                "3. Détails d'un tournoi\n"
                                )
        return menu_choice

    def tournament_details(self, tournaments):
        """_summary_
        ask for tournament's name
        Returns:
            str: tournament's name
        """
        while True:
            menu_choice = input("Saisir le nom du tournoi : ")
            for tournament in tournaments:
                if tournament["name"] == menu_choice:
                    return menu_choice
            print("Ce tournoi n'existe pas, veuillez renseigner un nom valide")


class Report():
    def player_list(self, players):
        """_summary_
        Displays a list of all players in alphabetical order
        Args:
            players (list[Player]): list of class' player
        """
        for player in players:
            print(player.last_name, player.first_name)

    def tournament_list(self, tournaments):
        """_summary_
        Display a liste of all tournaments' name, location, start date, description
        Args:
            tournaments (list[dict]): _description_
        """
        for tournament in tournaments:
            print(tournament["name"], tournament["location"], tournament["start_date"], tournament["description"])

    def tournament_details(self, tournament):
        """_summary_
        Displays details about a specific tournament
        Args:
            tournament (Tournament): class' tournament
        """
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
