import numpy as np
import networkx as nx
import random

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


    def generate_dungeon(self, room_attempts=30, min_size=5, max_size=10):
        self.tiles[:, :] = 1  # Start with all walls
        self.walkable[:, :] = False
        self.rooms = []
        centers = []

        for _ in range(room_attempts):
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            new_room = (x, y, w, h)

            # Check for overlap
            if any(self._rooms_overlap(new_room, other) for other in self.rooms):
                continue

            self._carve_room(new_room)
            self.rooms.append(new_room)
            centers.append((x + w // 2, y + h // 2))

        # Connect rooms using MST over centers
        g = nx.Graph()
        for i, (x1, y1) in enumerate(centers):
            for j, (x2, y2) in enumerate(centers):
                if i < j:
                    dist = abs(x1 - x2) + abs(y1 - y2)
                    g.add_edge(i, j, weight=dist)
        mst = nx.minimum_spanning_tree(g)

        for i, j in mst.edges:
            self._carve_corridor(centers[i], centers[j])

        # Update walkability and graph
        self.walkable = self.tiles == 0
        self._build_graph()

    def _carve_room(self, room):
        x, y, w, h = room
        self.tiles[y:y+h, x:x+w] = 0

    def _rooms_overlap(self, a, b, padding=1):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return (ax < bx + bw + padding and ax + aw + padding > bx and
                ay < by + bh + padding and ay + ah + padding > by)

    def _carve_corridor(self, start, end):
        x1, y1 = start
        x2, y2 = end
        if random.random() < 0.5:
            self._carve_horiz(x1, x2, y1)
            self._carve_vert(y1, y2, x2)
        else:
            self._carve_vert(y1, y2, x1)
            self._carve_horiz(x1, x2, y2)

    def _carve_horiz(self, x1, x2, y):
        if x1 > x2:
            x1, x2 = x2, x1
        self.tiles[y, x1:x2+1] = 0

    def _carve_vert(self, y1, y2, x):
        if y1 > y2:
            y1, y2 = y2, y1
        self.tiles[y1:y2+1, x] = 0