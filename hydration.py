import sense_hat

TIMER = 0
AWAKE_TIME = 14 * 3600


def get_thirst(glasses_per_day: int) -> float:
    """Calculate the thirst level based on the history of drinks."""
    seconds_between_drinks = AWAKE_TIME / glasses_per_day
    update_thirst(1)
    thirst = TIMER / seconds_between_drinks
    return min(1.0, thirst)


def reset_timer() -> None:
    """Reset the timer."""
    global TIMER
    TIMER = 0


def update_thirst(seconds: int) -> None:
    """Update the thirst level based on the time passed."""
    global TIMER
    TIMER += seconds * temperature_rate() * humidity_rate()


def get_temperature() -> float:
    """Get the current temperature."""
    sense = sense_hat.SenseHat()
    return sense.get_temperature()


def get_humidity() -> float:
    """Get the current humidity."""
    sense = sense_hat.SenseHat()
    return sense.get_humidity()


def temperature_rate() -> float:
    """Return the rate of temperature."""
    temp = get_temperature()
    if temp >= 35:
        return 1.75
    elif temp >= 30:
        return 1.5
    elif temp >= 25:
        return 1.25
    elif temp >= 20:
        return 1.0
    else:
        return 0.9


def humidity_rate() -> float:
    """Return the rate of humidity."""
    humidity = get_humidity()
    if humidity >= 70:
        return 2.0
    elif humidity >= 60:
        return 1.75
    elif humidity >= 50:
        return 1.25
    elif humidity >= 30:
        return 1.0
    else:
        return 1.5
