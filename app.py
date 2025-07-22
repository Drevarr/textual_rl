from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from map_widget import MapWidget
from engine import Engine
from gamemap import GameMap
from entity import Entity
from datetime import datetime


class RoguelikeApp(App):
    CSS_PATH = "ui/styles.tcss"

    def compose(self) -> ComposeResult:
        game_map = GameMap(40, 20)
        player = Entity(x=20, y=8, char='@', name='Player')
        enemy = Entity(x=15, y=11, char='E', name='Enemy', color='red')

        engine = Engine(game_map, player)
        engine.add_entity(enemy)

        yield Header(show_clock=True)
        yield MapWidget(engine)
        yield RichLog(highlight=True, markup=True, wrap=True)
        yield Footer()

    def log_action(self, kind: str, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {
            "movement": "green",
            "combat": "red",
            "loot": "yellow",
        }.get(kind, "white")
        formatted = f"[dim]{timestamp}[/dim] [bold {color}]{message}[/bold {color}]"
        self.query_one(RichLog).write(formatted)


if __name__ == "__main__":
    RoguelikeApp().run()
