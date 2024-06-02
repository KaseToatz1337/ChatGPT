class Response:

    def __init__(self, text: str, historyID: str, user: bool = False) -> None:
        self.text = text
        self.historyID = historyID
        self.user = user