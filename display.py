import sense_hat

sense = sense_hat.SenseHat()

Color = tuple[int, int, int]
MATRIX_SIZE = 8
WATER_ROWS = 4
BLACK = (0, 0, 0)
GLASSES_COLOR = (0, 0, 255)
HISTORY_COLOR = (255, 0, 255)
THIRST_MIN_COLOR = (0, 255, 0)
THIRST_MAX_COLOR = (255, 0, 0)


def display_glasses(glasses_count: int) -> None:
    """Display the number of glasses drunk."""
    assert 0 <= glasses_count <= MATRIX_SIZE * WATER_ROWS, "Invalid glasses count"
    for x in range(MATRIX_SIZE):
        for y in range(WATER_ROWS):
            position = y + x * WATER_ROWS
            color = GLASSES_COLOR if position < glasses_count else BLACK
            sense.set_pixel(x, y, color)


def display_history_bar(days_in_past: int) -> None:
    """Display a bar indicating the day currently displayed."""
    assert 0 <= days_in_past <= MATRIX_SIZE, "Invalid day"
    HISTORY_Y = WATER_ROWS
    for x in range(MATRIX_SIZE):
        color = BLACK if x < MATRIX_SIZE - days_in_past else HISTORY_COLOR
        sense.set_pixel(x, HISTORY_Y, color)


def display_thirst(thirst: float) -> None:
    """Display a colorful block indicating the thirst level."""
    assert 0 <= thirst <= 1, "Invalid thirst"
    color = _get_thirst_color(thirst)
    for x in range(MATRIX_SIZE):
        for y in range(WATER_ROWS + 1, MATRIX_SIZE):
            sense.set_pixel(x, y, color)


def _get_thirst_color(thirst: float) -> Color:
    return _interpolate_color(THIRST_MIN_COLOR, THIRST_MAX_COLOR, thirst)


def _interpolate_color(color1: Color, color2: Color, frac: float) -> Color:
    return tuple(
        int(channel1 * (1 - frac) + channel2 * frac)
        for channel1, channel2 in zip(color1, color2)
    )
