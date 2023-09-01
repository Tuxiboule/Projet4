"""fuctions helping the view"""

from datetime import datetime


def give_date():
    date = datetime.now()
    returned_date = (f"{date.day}/{date.month}/{date.year} - "f"{date.hour}:{date.minute}:{date.second}")
    return returned_date
