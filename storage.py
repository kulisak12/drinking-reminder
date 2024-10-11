import dataclasses
import datetime as dt
import pickle

STATE_FILE = "state.pickle"


@dataclasses.dataclass()
class State:
    history: list[dt.datetime] = dataclasses.field(default_factory=list)
    day_displayed: dt.date = dt.date.today()
    glasses_per_day: int = 12


def save_state(state: State) -> None:
    pickle.dump(state, open(STATE_FILE, "wb"))


def load_state() -> State:
    try:
        return pickle.load(open(STATE_FILE, "rb"))
    except FileNotFoundError:
        return State()
