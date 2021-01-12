from DataModels.PlayerDataModel import Player
from DataModels.ScoreDataModel import WTCScoreSystem
from DataModels.GameDataModel import Game
from DataModels.RoundDataModel import Round

import unittest
from PairingAlgorithms.PairingManager import SwissPairingManager


horus = Player(player_id='asdsa', name='Horus', nickname='Warmaster', score=WTCScoreSystem(), opponents_ids=[])
lion = Player(player_id='lolion', name='Lion', nickname='Traitor', score=WTCScoreSystem(), opponents_ids=[])
robot = Player(player_id='robosm', name='Roboute', nickname='PosterBoy', score=WTCScoreSystem(), opponents_ids=[])
bay = Player(player_id='sth', name='bay', nickname='Dummy', score=WTCScoreSystem(), opponents_ids=[])

pm = SwissPairingManager()


class PairingManagerBayTester(unittest.TestCase):

    def test_add_bay_odd_list(self):
        players = [horus, lion, robot]
        self.assertEqual(len(pm._add_bay_if_needed(players)), 4)

    def test_add_bay_even_list(self):
        players = [horus, lion]
        self.assertEqual(len(pm._add_bay_if_needed(players)), 2)

    def test_removing_bay_when_not_necessary(self):
        players = [horus, lion, bay]
        self.assertEqual(len(pm._add_bay_if_needed(players)), 2)


class PairingManagerFirstRoundTester(unittest.TestCase):

    def test_list_content_obj_type(self):
        players = [horus, lion, robot, bay]
        self.assertIsInstance(pm._first_round_pairing(players)[0], Game)


class PairingManagerCreateRound(unittest.TestCase):

    def test_return_type(self):
        players = [horus, lion, robot, bay]
        list_of_games = pm._first_round_pairing(players)
        self.assertIsInstance(pm._create_round_object(list_of_games), Round)


if __name__ == '__main__':
    unittest.main()