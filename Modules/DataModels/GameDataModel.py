from dataclasses import dataclass, field
from enum import Enum
from dataclasses_json import dataclass_json
from typing import List, Tuple
import uuid


class GameStatuses(Enum):
    Ongoing = 1
    Finished = 2


@dataclass_json
@dataclass
class Game:
    game_id: uuid = field(default_factory=tuple)
    game_status: GameStatuses = GameStatuses
    game_participants: List[Tuple] = field(default_factory=list)

    def export_game_participants(self) -> List:
        participants = [self.game_participants[0][0], self.game_participants[1][0]]
        return participants


if __name__ == '__main__':
    game_1 = Game(
        game_id=uuid,
        game_status=GameStatuses(1),
        game_participants=[('Player1', 26), ("Player2", 25)]
    )


