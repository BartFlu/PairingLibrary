from abc import ABC, abstractmethod
from DataModels.RoundDataModel import Round, RoundStatuses
from DataModels.GameDataModel import Game, GameStatuses
from DataModels.PlayerDataModel import Player
from DataModels.ScoreDataModel import WTCScoreSystem
from typing import List
from datetime import datetime
import uuid
import random


class PairingManager(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_round(self, round_n: int, players: List) -> Round:
        pass

    @abstractmethod
    def end_round(self, round: Round) -> List:
        pass

    @staticmethod
    @abstractmethod
    def delete_round(round_id: str):
        pass


class SwissPairingManager(PairingManager):

    def __init__(self):
        super().__init__()
        pass

    def create_round(self, round_n: int, players: List) -> Round:

        players = self._add_bay_if_needed(players)
        if round_n == 1:
            list_of_games = self._first_round_pairing(players)
        else:
            list_of_games = self._non_first_round_pairing(players)
        created_round = self._create_round_object(list_of_games)
        return created_round

    @staticmethod
    def _add_bay_if_needed(list_of_players: List):
        players = [player for player in list_of_players if player.name != 'bay']
        if len(players) % 2 != 0:
            bay = Player(player_id=uuid.uuid4(),
                         name='bay',
                         nickname=None,
                         score=WTCScoreSystem(),
                         opponents_ids=[])
            players.append(bay)

            return players
        return players

    @staticmethod
    def _first_round_pairing(players: List) -> List:
        list_of_games = []
        random.shuffle(players)
        for i, k in zip(players[0::2], players[1::2]):
            player1 = (i, i.score)
            player2 = (k, k.score)
            game = Game(game_id=uuid.uuid4(),
                        game_status=GameStatuses(1),
                        game_participants=[player1, player2])

            list_of_games.append(game)
        return list_of_games

    def _non_first_round_pairing(self, players: List) -> List:
        list_of_games = []
        players_sorted_by_score = self._sort_players_by_score(players)
        while len(players_sorted_by_score) > 0:
            player1 = players_sorted_by_score.pop(0)  # return the player with the highest score
            possible_opponents = [x for x in players_sorted_by_score if x.player_id not in player1.opponents_ids]
            player2 = possible_opponents[0]
            players_sorted_by_score.remove(player2)
            player1 = (player1, player1.score)
            player2 = (player2, player2.score)
            game = Game(game_id=uuid.uuid4(),
                        game_status=GameStatuses(1),
                        game_participants=[player1, player2])

            list_of_games.append(game)
        return list_of_games

    @staticmethod
    def _sort_players_by_score(players: List) -> List:
        players.sort(key=lambda x: x.score.comparison_points(), reverse=True)
        return players

    @staticmethod
    def _create_round_object(games_in_round: List) -> Round:
        created_round = Round(round_id=uuid.uuid4(),
                              ts_start=datetime.now().timestamp(),
                              ts_end=None,
                              round_status=RoundStatuses(1),
                              games_in_round=games_in_round
                              )
        return created_round

    def end_round(self, round: Round) -> List:
        finished_round = self._set_round_end_time_and_status(round)
        #db.update_round(finished_round)
        all_players_in_round = round.show_all_players()
        return all_players_in_round

    @staticmethod
    def _set_round_end_time_and_status(round: Round) -> Round:
        round.add_end_time()
        round.change_status_to_finished()
        return round

    @staticmethod
    def delete_round(round_id: str):
        return NotImplemented