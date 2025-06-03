from random import randint


class State:
    states: list = ["MAIN_MENU", "WATER", "POLUTION", "TEMPERATURE"]
    state: str = "MAIN_MENU"
    image: int = 1

    running: bool = True

    @classmethod
    def change_state(cls, state: str) -> None:
        if state in cls.states:
            cls.image = randint(1, 2)
            cls.state = state
        else:
            raise ValueError(
                f"State error: {state} don't exist. Correct states: {cls.states}"
            )

    @classmethod
    def toggle_run_state(cls, run: bool) -> None:
        cls.running = run
