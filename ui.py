from textual.widgets import RichLog

class GameLog(RichLog):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("highlight", True)
        kwargs.setdefault("markup", True)
        kwargs.setdefault("wrap", True)
        super().__init__(*args, **kwargs)
