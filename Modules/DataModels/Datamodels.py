from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
import uuid
from datetime import datetime



class RoundStatuses(Enum):
    Ongoing = 'Ongoing'
    Finished = 'Finished'


class GameStatuses(Enum):
    Ongoing = 'Ongoing'
    Finished = 'Finished'


class ScoreBase(ABC):

    def __init__(self, points=0):
        self.id: Optional[int] = None
        self.points = points
        self.tiebreakers = 0

    @abstractmethod
    def change_points(self, points: int):
        pass

    @abstractmethod
    def change_tiebreakers(self, points: int):
        pass


class WTCScoreSystem(ScoreBase):

    def __init__(self, points=0, tiebreakers=0):
        super().__init__(points=points)
        self.tiebreakers = tiebreakers

    def __repr__(self):
        return f'Points: {self.points}, tiebreakers: {self.tiebreakers}'

    def comparison_points(self):
        return float(f'{self.points}.{self.tiebreakers}')

    def change_points(self, points: int):
        self.points = points

    def change_tiebreakers(self, tiebreakers: int):
        self.tiebreakers = tiebreakers


@dataclass_json
@dataclass
class Player:
    id: Optional[int] = None
    player_id: uuid = field(default_factory=tuple)
    name: str = '',
    nickname: Optional[str] = '',
    score: ScoreBase = ScoreBase,
    opponents_ids: List[str] = field(default_factory=list)

    def __repr__(self):
        return self.name

    def edit_score(self, points: int, tiebreakers: int):
        self.score.change_points(points)
        self.score.change_tiebreakers(tiebreakers)


@dataclass_json
@dataclass
class Game:

    game_id: uuid = field(default_factory=tuple)
    game_status: GameStatuses = GameStatuses
    game_participants: List[Tuple[Player, ScoreBase]] = field(default_factory=list)

    def export_game_participants(self) -> List[Player]:
        participants = [self.game_participants[0][0], self.game_participants[1][0]]
        return participants


@dataclass_json
@dataclass
class Round:
    id: Optional[int] = None
    round_id: uuid.uuid4 = field(default_factory=tuple)
    ts_start: datetime.timestamp = datetime
    ts_end: Optional[datetime.timestamp] = datetime
    round_status: RoundStatuses = RoundStatuses
    games_in_round: List[Game] = field(default_factory=list)

    def add_end_time(self):
        self.ts_end = datetime.now().timestamp()

    def change_status_to_finished(self):
        self.round_status = RoundStatuses.Finished

    def show_all_players(self) -> List:
        list_of_players = []
        for game in self.games_in_round:
            list_of_players.append(game.export_game_participants())
        return list_of_players
