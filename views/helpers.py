"""fuctions helping the view"""

from datetime import datetime


def give_date():
    """_summary_
    Gives current date and hour
    Returns:
        str: date and horu format DD/MM/YYY - HH:MM:SS
    """
    date = datetime.now()
    returned_date = (f"{date.day}/{date.month}/{date.year} - "f"{date.hour}:{date.minute}:{date.second}")
    return returned_date
