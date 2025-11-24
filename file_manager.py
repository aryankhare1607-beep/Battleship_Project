import json
from typing import Any, Dict, Optional

class FileManager:
    def __init__(self, result_filename: str = "battleship_save.txt", state_filename: str = "battleship_state.json"):
        self.result_filename = result_filename
        self.state_filename = state_filename

    def save_result(self, text: str) -> None:
        with open(self.result_filename, "w") as f:
            f.write(text)

    def save_state(self, state: Dict[str, Any]) -> None:
        with open(self.state_filename, "w") as f:
            json.dump(state, f)

    def load_state(self) -> Optional[Dict[str, Any]]:
        try:
            with open(self.state_filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
