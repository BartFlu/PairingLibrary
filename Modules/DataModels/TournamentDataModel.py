from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
import uuid
from datetime import datetime


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
    total_score: ScoreBase = ScoreBase
    opponents_ids: List[str] = field(default_factory=list)

    def __repr__(self):
        if self.nickname:
            name = self.name.split()
            return f'{name[0]} \'{self.nickname}\' {name[1]}'
        else:
            return self.name

    def edit_score(self, points: int, tiebreakers: int):
        self.score.change_points(points)
        self.score.change_tiebreakers(tiebreakers)

    def calculate_total_score(self):
        self.total_score.points += self.score.points
        self.total_score.tiebreakers += self.score.tiebreakers


@dataclass_json
@dataclass
class Game:

    class GameStatuses(Enum):
        ONGOING = 'Ongoing'
        FINISHED = 'Finished'

    game_id: uuid = field(default_factory=tuple)
    game_status: GameStatuses = GameStatuses
    game_participants: List[Tuple[Player, ScoreBase]] = field(default_factory=list)

    def edit_players_score(self, pl1_points: int, pl1_tiebreakers: int, pl2_points: int, pl2_tiebreakers: int):
        participants = self.export_game_participants()
        participants[0].edit_score(points=pl1_points, tiebreakers=pl1_tiebreakers)
        participants[1].edit_score(points=pl2_points, tiebreakers=pl2_tiebreakers)

    def export_game_participants(self) -> List[Player]:
        participants = [self.game_participants[0][0], self.game_participants[1][0]]
        return participants

    def end_game(self):
        self.game_status = Game.GameStatuses.FINISHED
        self._save_player_opponent()
        self._set_players_total_score()

    def _save_player_opponent(self):
        player1 = self.game_participants[0][0]
        player2 = self.game_participants[1][0]
        player1.opponents_ids.append(player2.player_id)
        player2.opponents_ids.append(player1.player_id)

    def _set_players_total_score(self):
        for player in self.export_game_participants():
            player.calculate_total_score()


@dataclass_json
@dataclass
class Round:

    class RoundStatuses(Enum):
        Ongoing = 'Ongoing'
        Finished = 'Finished'

    id: Optional[int] = None
    round_id: uuid.uuid4 = field(default_factory=tuple)
    ts_start: datetime.timestamp = datetime
    ts_end: Optional[datetime.timestamp] = datetime
    round_status: RoundStatuses = RoundStatuses
    games_in_round: List[Game] = field(default_factory=list)

    def finish_and_update_total_score(self):
        """
        Adds end time timestamp to self, sets status to finish, end games.
        :return:
        """
        self._add_end_time()
        self.round_status = Round.RoundStatuses.Finished
        for game in self.games_in_round:
            game.end_game()

    def _add_end_time(self):
        self.ts_end = datetime.now().timestamp()

    def show_all_players(self) -> List:
        """
        Show all players participating in the Round
        :return: a list of Player objecst
        """
        list_of_players = []
        for game in self.games_in_round:
            for player in game.export_game_participants():
                list_of_players.append(player)
        return list_of_players
