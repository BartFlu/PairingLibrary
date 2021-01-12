from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Optional
from DataModels.ScoreDataModel import ScoreBase
from DataModels.ScoreDataModel import WTCScoreSystem
import uuid


@dataclass_json
@dataclass
class Player:
    player_id: uuid = field(default_factory=tuple)
    name: str = '',
    nickname: Optional[str] = '',
    score: ScoreBase = ScoreBase,
    opponents_ids: List[str] = field(default_factory=list)

    def __repr__(self):
        return self.name


if __name__ == '__main__':

    bay = Player(player_id=uuid.uuid4(),
                 name='bay',
                 nickname=None,
                 score=WTCScoreSystem(),
                 opponents_ids=[])

    print(bay)