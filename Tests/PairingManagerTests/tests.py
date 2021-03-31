from DataModels.TournamentDataModel import ScoreBase, WTCScoreSystem, Player, Game, Round
from PairingLibrary.PairingManager import SwissPairingManager
from PairingLibrary.Tournament import Tournament
from typing import List
import unittest


horus = Player(player_id='asdsa', name='Horus', nickname='Warmaster', score=WTCScoreSystem(), opponents_ids=[])
lion = Player(player_id='lolion', name='Lion', nickname='Traitor', score=WTCScoreSystem(), opponents_ids=[])
robot = Player(player_id='robosm', name='Roboute', nickname='PosterBoy', score=WTCScoreSystem(), opponents_ids=[])
bay = Player(player_id='sth', name='bay', nickname='Dummy', score=WTCScoreSystem(), opponents_ids=[])

pm = SwissPairingManager()


class PairingManagerBayTester(unittest.TestCase):

    def test_add_bay_odd_list(self):
        players = [horus, lion, robot]
        self.assertEqual(len(pm._add_bay_if_needed(players, scoring_system=Tournament.ScoreTypes.WTC)), 4)

    def test_add_bay_even_list(self):
        players = [horus, lion]
        self.assertEqual(len(pm._add_bay_if_needed(players, scoring_system=Tournament.ScoreTypes.WTC)), 2)

    def test_removing_bay_when_not_necessary(self):
        players = [horus, lion, bay]
        self.assertEqual(len(pm._add_bay_if_needed(players, scoring_system=Tournament.ScoreTypes.WTC)), 2)


class PairingManagerFirstRoundTester(unittest.TestCase):

    def test_list_content_obj_type(self):
        players = [horus, lion, robot, bay]
        self.assertIsInstance(pm._first_round_pairing(players)[0], Game)


class PairingManagerCreateRound(unittest.TestCase):

    def test_return_type(self):
        players = [horus, lion, robot, bay]
        list_of_games = pm._first_round_pairing(players)
        self.assertIsInstance(pm._create_round_object(list_of_games), Round)


class TournamentTester(unittest.TestCase):

    t = Tournament()

    def test_set_pairing_method(self):
        TournamentTester.t.set_pairing_manager(Tournament.PairingTypes.SWISS)
        self.assertIsInstance(TournamentTester.t.pairing_manager, SwissPairingManager)

    def test_register_player(self):
        TournamentTester.t.register_player('Steve')
        self.assertEqual(len(TournamentTester.t.players), 1)

    def test_registered_player_type(self):
        self.assertIsInstance(TournamentTester.t.players[0], Player)

    def test_create_round_returned_type(self):
        TournamentTester.t.create_round()
        self.assertIsInstance(TournamentTester.t.current_round, Round)

    def test_first_round_change(self):
        self.assertEqual(TournamentTester.t.first_round, False)

    def test_round_end_returned_type(self):
        self.assertIsInstance(TournamentTester.t.end_round(), Round)


if __name__ == '__main__':
    unittest.main()
