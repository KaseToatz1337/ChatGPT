class RequiresLogin(Exception):

    def __init__(self) -> None:
        super().__init__("You must be logged in before calling this function.")