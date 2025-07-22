import numpy as np
import networkx as nx


class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # 0 = floor, 1 = wall
        self.tiles = np.zeros((height, width), dtype=np.uint8)

        # Add test wall structure (you can change these)
        self.tiles[5:15, 10] = 1   # vertical wall
        self.tiles[10, 10:30] = 1  # horizontal wall

        # Walkable where tile is 0 (floor)
        self.walkable = self.tiles == 0

        self._build_graph()

    def _build_graph(self):
        self.graph = nx.grid_2d_graph(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                if not self.walkable[y, x]:  # Note: (y, x) for tiles but graph is (x, y)
                    self.graph.remove_node((x, y))

    def is_walkable(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.walkable[y, x]
        return False

    def find_path(self, start: tuple[int, int], end: tuple[int, int]):
        try:
            return nx.shortest_path(self.graph, start, end)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def render(self) -> list[str]:
        """Return a list of strings representing the map for display."""
        rows = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if self.tiles[y, x] == 1:
                    row += "#"
                else:
                    row += "."
            rows.append(row)
        return rows

