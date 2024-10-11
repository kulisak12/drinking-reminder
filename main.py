#!/usr/bin/env python3
import datetime as dt
import signal
import threading

import sense_hat

import display
import hydration
import storage

state: storage.State


def main() -> None:
    """Run the drinking reminder."""
    global state
    state = storage.load_state()
    change_day(dt.date.today())

    # a thread that runs continuously and updates the thirst level
    threading.Thread(target=update_thirst, daemon=True).start()

    # the main thread handles callbacks
    configure_callbacks()
    signal.pause()


def change_day_forward() -> None:
    """Show the next day in history."""
    if state.day_displayed < dt.date.today():
        change_day(state.day_displayed + dt.timedelta(days=1))


def change_day_backward() -> None:
    """Show the previous day in history."""
    MAX_DAYS_IN_PAST = display.MATRIX_SIZE
    if (dt.date.today() - state.day_displayed).days < MAX_DAYS_IN_PAST:
        change_day(state.day_displayed - dt.timedelta(days=1))


def change_day(day: dt.date) -> None:
    """Show the history for the given day."""
    state.day_displayed = day
    glasses_count = count_glasses(day)
    days_in_past = (dt.date.today() - day).days
    display.display_glasses(glasses_count)
    display.display_history_bar(days_in_past)


def count_glasses(day: dt.date) -> int:
    """Count the glasses drunk on a given day."""
    return len([x for x in state.history if x.date() == day])


def register_glass() -> None:
    """Register a glass drunk now."""
    timestamp = dt.datetime.now().replace(microsecond=0)
    state.history.append(timestamp)
    change_day(dt.date.today())
    thirst = hydration.get_thirst(state.history, state.glasses_per_day)
    display.display_thirst(thirst)
    storage.save_state(state)


def update_thirst() -> None:
    """Periodically update the thirst level."""
    while True:
        thirst = hydration.get_thirst(state.history, state.glasses_per_day)
        display.display_thirst(thirst)
        threading.Event().wait(5)


def configure_callbacks() -> None:
    sense = sense_hat.SenseHat()
    sense.stick.direction_left = on_pressed(change_day_backward)
    sense.stick.direction_right = on_pressed(change_day_forward)
    sense.stick.direction_middle = on_pressed(register_glass)


def on_pressed(func):
    """A decorator to call a function only for the joystick's pressed action.

    Otherwise, the joystick triggers hold and release events as well.
    """
    def wrapper(event: sense_hat.InputEvent) -> None:
        if event.action == sense_hat.ACTION_PRESSED:
            func()
    return wrapper


if __name__ == "__main__":
    main()
