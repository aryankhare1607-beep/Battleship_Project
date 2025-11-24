from typing import List, Tuple
from ship import Ship

Grid_size = 10

class Board:
    def _init_(self):
        self.ships: List[Ship] = []
        self.hits = set()   
        self.misses = set() 

    def place_ship(self, ship: Ship, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        x1, y1 = start
        x2, y2 = end

        # must be straight line
        if x1 != x2 and y1 != y2:
            return False

        coords = []
        if x1 == x2:
            if y2 >= y1:
                step = 1
            else:
                step = -1
            length = abs(y2 - y1) + 1
            if length != ship.size:
                return False
            for y in range(y1, y2 + step, step):
                coords.append((x1, y))
        else:
            if x2 >= x1:
                step = 1
            else:
                step = -1
            length = abs(x2 - x1) + 1
            if length != ship.size:
                return False
            for x in range(x1, x2 + step, step):
                coords.append((x, y1))

        # checking if out of bounds or overlapping coords
        for (x, y) in coords:
            if not (0 <= x < Grid_size and 0 <= y < Grid_size):
                return False
            for s in self.ships:
                if (x, y) in s.coordinates:
                    return False

        ship.place(coords)
        self.ships.append(ship)
        return True

    # For random placement
    def placeRandomly(self, ship: Ship, start_x: int, start_y: int, horizontal: bool) -> bool:
        if horizontal:
            end = (start_x + ship.size - 1, start_y)
        else:
            end = (start_x, start_y + ship.size - 1)
        return self.place_ship(ship, (start_x, start_y), end)

    def register_attack(self, x: int, y: int) -> str:
        pos = (x, y)

        # prevents repeating a previous attack
        if pos in self.hits or pos in self.misses:
            return "repeat"

        # checking if ship is hit
        for ship in self.ships:
            if ship.occupies(pos):
                ship.register_hit(pos)
                self.hits.add(pos)
                if ship.is_sunk():
                    return f"sunk:{ship.name}:{ship.symbol}"
                return "hit"

        # else miss
        self.misses.add(pos)
        return "miss"

    def all_sunk(self) -> bool:
        return all(s.is_sunk() for s in self.ships)

    # Saving for JSON
    def save_data(self) -> dict:
        return {
            "ships": [s.save_data() for s in self.ships],
            "hits": list(self.hits),
            "misses": list(self.misses),
        }
    
    # Loading from JSON
    def load_data(data: dict) -> "Board":
        board = Board()
        board.ships = [Ship.load_data(x) for x in data.get("ships", [])]
        board.hits = set(tuple(p) for p in data.get("hits", []))
        board.misses = set(tuple(p) for p in data.get("misses", []))
        return board