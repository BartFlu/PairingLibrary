from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Optional
from datetime import datetime
from Modules.DataModels.GameDataModel import Game
import uuid

from enum import Enum


class RoundStatuses(Enum):
    Ongoing = 1
    Finished = 2


@dataclass_json
@dataclass
class Round:
    round_id: uuid.uuid4 = field(default_factory=tuple)
    ts_start: datetime.timestamp = datetime
    ts_end: Optional[datetime.timestamp] = datetime
    round_status: RoundStatuses = RoundStatuses
    games_in_round: List[Game] = field(default_factory=list)

    def add_end_time(self):
        self.ts_end = datetime.now().timestamp()

    def change_status_to_finished(self):
        self.round_status = RoundStatuses(2)

    def show_all_players(self) -> List:
        list_of_players = []
        for game in self.games_in_round:
            list_of_players.append(game.export_game_participants())
        return list_of_players


if __name__ == '__main__':
    pass
