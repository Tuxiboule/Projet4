from colorama import init, Fore, Style

# Initialisez colorama
init(autoreset=True)

texte = "Texte à souligner"
texte_souligne = f"{Style.BRIGHT}{texte}{Style.RESET_ALL}{Style.UNDERLINE}"

print(texte_souligne)
