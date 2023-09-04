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