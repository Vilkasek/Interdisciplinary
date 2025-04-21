class State:
    states: list = ["MAIN_MENU", "APP"]
    state: str

    @classmethod
    def change_state(cls, state: str) -> None:
        cls.state = state
