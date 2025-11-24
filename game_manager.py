from board import Board, GRID_SIZE
from ship import Ship
from file_manager import FileManager
import random
from typing import Tuple, List, Optional

SHIP_TYPES = [("Carrier",5,"C"),("Battleship",4,"B"),("Cruiser",3,"R"),("Submarine",3,"S"),("Destroyer",2,"D")]

class GameManager:
    def __init__(self):
        self.boards = [Board(), Board()]
        self.current = 0
        self.fm = FileManager()

    # ------- Saving --------
    def save_state(self, path: Optional[str] = None):
        state = {
            "current": self.current,
            "boards": [b.save_data() for b in self.boards]
        }
        self.fm.save_state(state) if path is None else self.fm.save_state_to(path, state)

    # ------- Loading -------
    def load_state(self):
        data = self.fm.load_state()
        if data is None:
            return None
        self.current = data.get("current", 0)
        self.boards = [Board.load_data(bd) for bd in data.get("boards", [])]
        return data

    # ------- Random placement -------
    def random_setup(self, player: int) -> None:
        board = self.boards[player]
        for name, size, sym in SHIP_TYPES:
            placed = False
            attempts = 0
            while not placed and attempts < 1000:
                attempts += 1
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                horiz = random.choice([True, False])
                if horiz:
                    end = (x + size - 1, y)
                else:
                    end = (x, y + size - 1)
                ship = Ship(name, size, sym)
                placed = board.place_ship(ship, (x, y), end)
            if not placed:
                raise RuntimeError("Random placement failed after many tries.")

    # ------- Manual placement -------
    def place_ship_manual(self, player: int, ship_name: str, start: Tuple[int,int], end: Tuple[int,int]) -> bool:
        # find out which ship
        for name, size, sym in SHIP_TYPES:
            if name == ship_name:
                ship = Ship(name, size, sym)
                return self.boards[player].place_ship(ship, start, end)
        return False

    # ------- Attack logic -------
    def register_attack(self, defender: int, x: int, y: int) -> str:
        board = self.boards[defender]
        res = board.register_attack(x, y)
        if isinstance(res, str):
            return res
        if res is True:
            # hit
            # check if any ship is sunk at that position
            for s in board.ships:
                if (x, y) in s.coordinates and s.is_sunk():
                    return f"sunk:{s.name}:{s.symbol}"
            return "hit"
        elif res is False:
            return "miss"
        else:
            return str(res)

    def all_sunk(self, player: int) -> bool:
        return self.boards[player].all_sunk()

    # ------- Helper/Utility-------
    def get_board(self, player: int) -> Board:
        return self.boards[player]

    def reset(self):
        self.boards = [Board(), Board()]
        self.current = 0

# convenience for simple imports
gm = GameManager()
