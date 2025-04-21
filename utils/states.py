class State:
    states: list = ["MAIN_MENU", "APP"]
    state: str

    @classmethod
    def change_state(cls, state: str) -> None:
        if state in cls.states:
            cls.state = state
        # TODO: Add error handling
