import datetime as dt

import storage


def before_hours(hours: int) -> dt.datetime:
    return dt.datetime.now().replace(microsecond=0) - dt.timedelta(hours=hours)

history = [
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 3),
    before_hours(2 * 24 + 2),
    before_hours(2 * 24 + 1),
    before_hours(1 * 24 + 2),
    before_hours(1 * 24 + 1),
    before_hours(0 * 24 + 4),
    before_hours(0 * 24 + 3),
    before_hours(0 * 24 + 2),
    before_hours(0 * 24 + 1),
]
state = storage.State(history=history)
storage.save_state(state)
