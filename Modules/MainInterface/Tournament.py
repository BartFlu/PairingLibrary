from typing import List
from enum import Enum
from typing import Optional
from PairingAlgorithms.PairingManager import PairingManager
import uuid


class PairingMethods(Enum):
    Swiss: 1


class Tournament:

    def __init__(self, num_of_rounds: int, players: List):
        self.num_of_rounds = num_of_rounds
        self.players = players
        self.round_number = 1
        self.pairing_manager = PairingManager()
        self.db =

    def register_player(self, name: str, nickname: Optional[str]=None):
        player =
        self.players.append()
        return NotImplemented

    def unregister_player(self, player_id: str):
        self.players = [x for x in self.players if x.player_id != player_id]

    def create_round(self):
        new_round = self.pairing_manager.create_round(self.round_number, self.players)
        self.round_number += 1
        return new_round

    def delete_round(self, round_id: str):
        self.round_number -= 1
        return self.pairing_manager.delete_round(round_id)

    @staticmethod
    def update_game(game_id: str, pl1_points, pl1_tiebreakers, pl2_points, pl2_tiebreakers):

        return NotImplemented

    def set_pairing_method(self, pairing_manager: PairingManager):
        self.pairing_manager = pairing_manager

