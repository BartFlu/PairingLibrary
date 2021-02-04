from typing import List
from enum import Enum
from typing import Optional
from PairingLibrary.PairingManager import PairingManager, SwissPairingManager
from DataModels.Datamodels import Round, Player, ScoreBase, WTCScoreSystem
import uuid


class PairingEnum(Enum):
    Swiss = SwissPairingManager()


class ScoreEnum(Enum):
    WTC = WTCScoreSystem()


class Tournament:

    def __init__(self, num_of_rounds: int):
        self.num_of_rounds = num_of_rounds
        self.players: List[Player] = []
        self.round_number = 0
        self.pairing_manager: PairingManager = SwissPairingManager()
        self.db = None
        self.round: Optional[Round] = None

    def register_player(self, name: str, score: ScoreEnum, nickname: Optional[str] = None):
        player = self._create_player(name=name, nickname=nickname, score=score)
        self.players.append(player)
        return player.player_id

    def _create_player(self, name: str, score: ScoreEnum, nickname: Optional[str]) -> Player:
        player = Player(player_id=uuid.uuid4(),
                        name=name,
                        nickname=nickname,
                        score=self._create_score(score),
                        opponents_ids=[])
        return player

    @staticmethod
    def _create_score(score: ScoreEnum) -> ScoreBase:
        return score.value

    def unregister_player(self, player_id: str):
        self.players = [x for x in self.players if x.player_id != player_id]

    def create_round(self):
        self.round_number += 1
        new_round = self.pairing_manager.create_round(self.round_number, self.players)
        self.round = new_round
        return new_round

    def delete_round(self):
        self.round_number -= 1
        self.round = None

    def end_round(self):
        self.players = self.pairing_manager.get_final_results(self.round)
        self.round = None
        return self.players

    def update_players_score(self, game_id: str, pl1_points, pl1_tiebreakers, pl2_points, pl2_tiebreakers):
        game = [x for x in self.round.games_in_round if x.game_id == game_id][0]
        players = game.export_game_participants()
        players[0].edit_score(pl1_points, pl1_tiebreakers)
        players[1].edit_score(pl2_points, pl2_tiebreakers)

    def set_pairing_manager(self, pairing_type: PairingEnum):
        self.pairing_manager = self._set_pairing_manager(pairing_type)

    @staticmethod
    def _set_pairing_manager(pairing_type: PairingEnum) -> PairingManager:
        return pairing_type.value
