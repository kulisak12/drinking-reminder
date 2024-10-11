import datetime as dt


def get_thirst(history: list[dt.datetime], glasses_per_day: int) -> float:
    """Calculate the thirst level based on the history of drinks."""
    AWAKE_TIME = 16 * 3600
    seconds_between_drinks = AWAKE_TIME / glasses_per_day
    last_drink = history[-1] if history else dt.datetime.now()
    seconds_without_drink = (dt.datetime.now() - last_drink).total_seconds()
    thirst = seconds_without_drink / seconds_between_drinks
    return min(1.0, thirst)
