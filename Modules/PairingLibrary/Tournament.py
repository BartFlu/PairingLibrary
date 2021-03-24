from typing import List
from enum import Enum
from typing import Optional
from PairingLibrary.PairingManager import PairingManager, SwissPairingManager
from DataModels.TournamentDataModel import Round, Player, ScoreBase, WTCScoreSystem
import uuid


class Tournament:

    class PairingTypes(Enum):
        SWISS = SwissPairingManager

    class ScoreTypes(Enum):
        WTC = WTCScoreSystem

    def __init__(self, pairing_manager: PairingTypes = PairingTypes.SWISS, scoring_system: ScoreTypes = ScoreTypes.WTC):
        self.first_round = True
        self.players: List[Player] = []  # TODO Listę graczy można też zabstraktować robiąc osobną klasę przechowującą tę liste
        self.round_number = 0
        self.pairing_manager = pairing_manager.value()
        self.scoring_system = scoring_system
        self.db = None
        self.current_round: Optional[Round] = None
        self.past_rounds: List = []

    def register_player(self, name: str, nickname: Optional[str] = None):
        """
        Create Player object and add it to self.players.

        :param name: Player name as string
        :param score: Score class as Enum. It is now hardcoded as WTC scoring becouse it's the only one implemented
        :param nickname: Optional, nickname as string
        :return: player id (UUID)
        """
        player = self._create_player(name=name, nickname=nickname)
        self.players.append(player)
        return player.player_id

    def _create_player(self, name: str, nickname: Optional[str]) -> Player:
        return Player(player_id=uuid.uuid4(), name=name,
                      nickname=nickname,
                      score=self.scoring_system.value(),
                      total_score=self.scoring_system.value(),
                      opponents_ids=[])

    def unregister_player(self, player_id: str) -> bool:
        """
        Note: this method deletes player from self.players so it will have no effect on the current round.
        :param player_id:
        :return: Returns True if deleted player.
        """
        init_players = len(self.players)
        self.players = [x for x in self.players if x.player_id != player_id]
        after_delete = len(self.players)
        return True if init_players > after_delete else False

    def create_round(self) -> Round:
        """
        Uses self.pairing_manager to create new Round object.
        :return: Round object
        """
        new_round = self.pairing_manager.create_round(self.first_round, self.players, self.scoring_system)
        if self.first_round:
            self.first_round = False
        self.current_round = new_round
        return new_round

    def end_round(self) -> Round:
        """
        Use self.pairing_manager to finish the current round (self.round). Finish means adding end timestamp to
        the round object, changing round status to finish, game statuses to finish, calculating players total score
        and registering player's opponent ids.
        Finished round is saved in self.past_rounds
        It then set self.round to None.
        :return: Finished Round object.
        """
        finished_round = self.pairing_manager.set_round_to_finished(self.current_round)
        self.delete_round()
        self.past_rounds.append(finished_round)
        return finished_round

    def delete_round(self):
        """Delete Round object"""
        self.current_round = None

    def show_results(self) -> List:
        """
        :return: List of tuples with players and their total score.
        """

        return [(x, x.total_score) for x in self.players]

    def get_games_in_the_round_list(self) -> List:
        return self.current_round.games_in_round

    def show_players_in_the_round(self) -> List:
        """
        Returns a list of players in the current round. Providing there is an ongoing round.
        :return: List of player objects.
        """
        return self.current_round.show_all_players()

    def update_players_score(self, game_id: str, pl1_points: int, pl1_tiebreakers: int,
                             pl2_points: int, pl2_tiebreakers: int):

        game = [x for x in self.current_round.games_in_round if x.game_id == game_id][0]
        players = game.export_game_participants()
        players[0].edit_score(pl1_points, pl1_tiebreakers)
        players[1].edit_score(pl2_points, pl2_tiebreakers)

    def set_pairing_manager(self, pairing_type: PairingTypes):
        """
        Change the pairing manager.
        :param pairing_type: declared as this class internal Enum.
        :return: The name of the current Pairing Maager class.
        """
        self.pairing_manager = self._set_pairing_manager(pairing_type)
        return self.pairing_manager

    @staticmethod
    def _set_pairing_manager(pairing_type: PairingTypes) -> PairingManager:
        return pairing_type.value()
