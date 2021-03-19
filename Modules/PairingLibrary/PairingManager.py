from abc import ABC, abstractmethod
from DataModels.Datamodels import WTCScoreSystem, Player, Round, Game
from typing import List
from datetime import datetime
import uuid
import random


class PairingManager(ABC):

    def __init__(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def create_round(self, round_n: int, players: List) -> Round:
        pass

    @staticmethod
    def get_final_results(game_round: Round) -> List:
        all_players_in_round = game_round.show_all_players()
        return all_players_in_round

    def set_round_to_finished(self, game_round: Round) -> Round:
        finished_round = self._finish_round_and_games(game_round)
        return finished_round

    @staticmethod
    def _finish_round_and_games(game_round: Round) -> Round:
        game_round.finish_and_update_total_score()
        return game_round


class SwissPairingManager(PairingManager):

    def __init__(self):
        super().__init__()
        pass

    def create_round(self, first_round: bool, players: List) -> Round:
        """
        Before the parings script checks if there is an even number of players and adds a 'dummy' if needed.
        In Swiss first round is a random draft of players, next rounds' pairing are based on player score.
        That's why this class checks if it's the first or non first  round.
        :param first_round:
        :param players:
        :return:
        """

        players = self._add_bay_if_needed(players)
        if first_round:
            list_of_games = self._first_round_pairing(players)
        else:
            list_of_games = self._non_first_round_pairing(players)
        created_round = self._create_round_object(list_of_games)
        return created_round

    @staticmethod
    def _add_bay_if_needed(list_of_players: List) -> List:
        """
        Adds a dummy player if num of players is not even. Before that checks if there is a dummy player already.
        :param list_of_players: A list of Player objects
        :return: A list of Player objects
        """
        players = [player for player in list_of_players if player.name != 'bay']
        if len(players) % 2 != 0:
            bay = Player(player_id=uuid.uuid4(),
                         name='bay',
                         nickname=None,
                         score=WTCScoreSystem(), # todo przyjmujesz tutaj WTC scora dla bye'a, ale to nie zawsze tak bedzie
                         opponents_ids=[])
            players.append(bay)

            return players
        return players

    @staticmethod
    def _first_round_pairing(players: List) -> List:
        """
        Shuffle player list and pair them randomly
        :param players: List of Player objects
        :return: A list of game objects
        """
        list_of_games = []
        random.shuffle(players)
        for i, k in zip(players[0::2], players[1::2]):
            player1 = (i, i.score)
            player2 = (k, k.score)
            game = Game(game_id=uuid.uuid4(),
                        game_status=Game.GameStatuses.Ongoing,  # TODO a nie lepiej bedzie mieć coś takiego Game.Statuses.ONGOING ??
                        game_participants=[player1, player2])

            list_of_games.append(game)
        return list_of_games

    def _non_first_round_pairing(self, players: List) -> List:
        """
        Sorts player by score, pick the player with the highest score and pick the next one from the pool of players
        he didn't play with. Remove the players from the initial pool and repeat the process.
        :param players: List of Player objects
        :return: list of Game objects
        """
        list_of_games = []
        players_sorted_by_score = self._sort_players_by_score(players)
        while len(players_sorted_by_score) > 0:
            player1 = players_sorted_by_score.pop(0)  # return the player with the highest score
            possible_opponents = [x for x in players_sorted_by_score if x.player_id not in player1.opponents_ids]  # TODO To jest bardzo ładne, podoba mi się :)
            player2 = possible_opponents[0]
            players_sorted_by_score.remove(player2)
            player1 = (player1, player1.score)
            player2 = (player2, player2.score)
            game = Game(game_id=uuid.uuid4(),
                        game_status=Game.GameStatuses.Ongoing,
                        game_participants=[player1, player2])

            list_of_games.append(game)
        return list_of_games

    @staticmethod
    def _sort_players_by_score(players: List) -> List:
        players.sort(key=lambda x: x.total_score.comparison_points(), reverse=True)
        return players

    @staticmethod
    def _create_round_object(games_in_round: List) -> Round:
        """

        :param games_in_round: list of game objects
        :return: Round object
        """
        created_round = Round(round_id=uuid.uuid4(),
                              ts_start=datetime.now().timestamp(),
                              ts_end=None,
                              round_status=Round.RoundStatuses.Ongoing,
                              games_in_round=games_in_round
                              )
        return created_round
