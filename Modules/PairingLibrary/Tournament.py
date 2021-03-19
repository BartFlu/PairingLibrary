from typing import List
from enum import Enum
from typing import Optional
from PairingLibrary.PairingManager import PairingManager, SwissPairingManager
from DataModels.Datamodels import Round, Player, ScoreBase, WTCScoreSystem
import uuid


class Tournament:

    # TODO jak w komentarzy w test scripts nie nazywja: PairingEnum, bo nie robisz też TournamentClass :)
    # TODO przyjętym jest standardem, że wartości enumów piszemy Capital Cases, czyli: SWISS
    class PairingEnum(Enum):
        Swiss = SwissPairingManager

    class ScoreEnum(Enum):
        WTC = WTCScoreSystem

    def __init__(self, pairing_manager: PairingEnum = PairingEnum.Swiss):
        self.first_round = True
        self.players: List[Player] = []  # TODO Listę graczy można też zabstraktować robiąc osobną klasę przechowującą tę liste
        self.round_number = 0
        self.pairing_manager = pairing_manager.value()
        self.db = None
        self.round: Optional[Round] = None  # TODO a nie lista rund???

    def register_player(self, name: str, score: ScoreEnum = ScoreEnum.WTC, nickname: Optional[str] = None):
        """
        Create Player object and add it to self.players.

        :param name: Player name as string
        :param score: Score class as Enum. It is now hardcoded as WTC scoring becouse it's the only one implemented
        :param nickname: Optional, nickname as string
        :return: player id (UUID)
        """
        player = self._create_player(name=name, nickname=nickname, score=score)  # TODO Scoring powinien być wartością prywatną klasy, bo kazdy player będzie miał w ramach turnieju ten sam typ scoringu
        self.players.append(player)
        return player.player_id

    def _create_player(self, name: str, score: ScoreEnum, nickname: Optional[str]) -> Player:
        player = Player(player_id=uuid.uuid4(),
                        name=name,
                        nickname=nickname,
                        score=self._create_score(score),
                        total_score=self._create_score(score),
                        opponents_ids=[])
        return player # TODO mozna skrócić i po prostu: return Player(...)

    @staticmethod
    def _create_score(score: ScoreEnum) -> ScoreBase:
        return score.value()  # TODO w pythonie czasem się nie pisze takich jednolinijkowych abstakcji, zwłaszcza jak to metoda prywatna

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
        new_round = self.pairing_manager.create_round(self.first_round, self.players)
        if self.first_round:
            self.first_round = False
        self.round = new_round
        return new_round

    def delete_round(self):
        """Delete Round object"""
        self.round = None  # todo ale że wszystkie rundy?

    def end_round(self) -> Round:
        """
        Use self.pairing_manager to finish the current round (self.round). Finish means adding end timestamp to
        the round object, changing round status to finish, game statuses to finish, calculating players total score
        and registering player's opponent ids.
        It then set self.round to None.
        :return: Finished Round object.
        """
        finished_round = self.pairing_manager.set_round_to_finished(self.round)
        self.round = None  # todo jak już uzywasz abstrakcji jak wyżej delete_round, to tutaj tego użyj
        return finished_round

    def show_results(self) -> List:
        """

        :return: List of tuples with players and their total score.
        """
        return self._show_results()  # todo a tego to już nie rozumiem, dwie metody takie same?

    def _show_results(self) -> List:
        results = [(x, x.total_score) for x in self.players]
        return results

    def show_games_in_the_round(self) -> List:
        return self.round.games_in_round  # todo te wszystkie funkcje nie pokazują gier, tylko zwracają listę gier, poprawna nazwa to get_games_in_the_round_list

    def show_players_in_the_round(self) -> List:
        """
        Returns a list of players in the current round. Providing there is an ongoing round.
        :return: List of player objects.
        """
        return self.round.show_all_players()

    def update_players_score(self, game_id: str, pl1_points: int, pl1_tiebreakers: int,
                             pl2_points: int, pl2_tiebreakers: int):

        game = [x for x in self.round.games_in_round if x.game_id == game_id][0]
        players = game.export_game_participants()
        players[0].edit_score(pl1_points, pl1_tiebreakers)
        players[1].edit_score(pl2_points, pl2_tiebreakers)

    def set_pairing_manager(self, pairing_type: PairingEnum):
        """
        Change the pairing manager.
        :param pairing_type: declared as this class internal Enum.
        :return: The name of the current Pairing Maager class.
        """
        self.pairing_manager = self._set_pairing_manager(pairing_type)
        return self.pairing_manager

    @staticmethod
    def _set_pairing_manager(pairing_type: PairingEnum) -> PairingManager:
        return pairing_type.value()
