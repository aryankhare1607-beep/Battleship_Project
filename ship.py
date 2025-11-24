from typing import List, Tuple

# A class for carrier,destroyer,ship,submarine,cruiser
class Ship:
    def __init__(self, name: str, size: int, symbol: str,
        coordinates=None, hits=None):
        self.name = name
        self.size = size
        self.symbol = symbol
        self.coordinates = coordinates if coordinates is not None else []
        self.hits = hits if hits is not None else set()

    # Returns string representation of an object
    def __repr__(self):
        return (f"Ship(name={self.name!r}, size={self.size!r}, "
                f"symbol={self.symbol!r}, coordinates={self.coordinates!r}, "
                f"hits={self.hits!r})")

    # Helps in comparing ships 
    def __eq__(self, other):
        if not isinstance(other, Ship):
            return False
        return (self.name == other.name and
                self.size == other.size and
                self.symbol == other.symbol and
                self.coordinates == other.coordinates and
                self.hits == other.hits)


    def place(self, coords: List[Tuple[int,int]]):
        self.coordinates = coords
        self.hits = set()

    def register_hit(self, pos: Tuple[int,int]) -> bool:
        if pos in self.coordinates:
            self.hits.add(pos)
            return True
        return False

    def is_sunk(self) -> bool:
        return set(self.coordinates) == self.hits

    def occupies(self, pos: Tuple[int,int]) -> bool:
        return pos in self.coordinates

    def save_data(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "symbol": self.symbol,
            "coordinates": list(self.coordinates) if self.coordinates is not None else [],
            "hits": list(self.hits) if self.hits is not None else [],
        }

    def load_data(data: dict) -> "Ship":
        ship = Ship(data["name"], data["size"], data["symbol"])
        ship.coordinates = [tuple(c) for c in data.get("coordinates", [])]
        ship.hits = set(tuple(h) for h in data.get("hits", []))
        return ship

