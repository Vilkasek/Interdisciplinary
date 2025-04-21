class State:
    states: list = ["MAIN_MENU", "APP"]
    state: str = "MAIN_MENU"

    @classmethod
    def change_state(cls, state: str) -> None:
        if state in cls.states:
            cls.state = state
        else:
            raise ValueError(
                f"State error: {state} don't exist. Correct states: {cls.states}"
            )
