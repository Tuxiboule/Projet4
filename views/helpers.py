"""fuctions helping the view"""
import re

from datetime import datetime


def give_date():
    """_summary_
    Gives current date and hour
    Returns:
        str: date and hour format DD/MM/YYY - HH:MM:SS
    """
    date = datetime.now()
    returned_date = (f"{date.day}/{date.month}/{date.year} - "f"{date.hour}:{date.minute}:{date.second}")
    return returned_date


def validate_input(prompt, regex_pattern):
    """_summary_

    Args:
        prompt (str): question aksed to user
        regex_pattern (str): regular expression

    Returns:
        str: answer from user
    """
    while True:
        user_input = input(prompt)
        if re.match(regex_pattern, user_input):
            return user_input
        else:
            print("Saisie éronée, veuillez renseigner une saisie valide")
