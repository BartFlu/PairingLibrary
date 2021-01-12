from DataModels.PlayerDataModel import Player
from DataModels.ScoreDataModel import WTCScoreSystem
from typing import List
from DataModels.GameDataModel import Game, GameStatuses
import uuid
from datetime import datetime

horus = Player(player_id='horus', name='Horus', nickname='Warmaster', score=WTCScoreSystem(points=20, tiebreakers=31), opponents_ids=['lolion', 'whity'])
lion = Player(player_id='lolion', name='Lion', nickname='Traitor', score=WTCScoreSystem(points=40, tiebreakers=80), opponents_ids=['horus', 'robosm'])
robot = Player(player_id='robosm', name='Roboute', nickname='PosterBoy', score=WTCScoreSystem(points=40, tiebreakers=81), opponents_ids=['whity', 'lolion'])
scar = Player(player_id='whity', name='Khan', nickname='FastandFurious', score=WTCScoreSystem(points=26, tiebreakers=38), opponents_ids=['robosm', 'horus'])
bay = Player(player_id='sth', name='bay', nickname='Dummy', score=WTCScoreSystem(), opponents_ids=[])
players = [horus, lion, robot, scar]

players.sort(key=lambda x: x.score.comparison_points(), reverse=True)
print(players)

#grab the first player from the list
#check whom he/she was playing against
#grab the next player from the list who is not in the list above

list_of_games = []
while len(players) > 0:
    player1 = players.pop(0) # return the player with the highest score
    possible_opponents = [x for x in players if x.player_id not in player1.opponents_ids]
    player2 = possible_opponents[0]
    players.remove(player2)
    player1 = (player1, player1.score)
    player2 = (player2, player2.score)
    game = Game(game_id=uuid.uuid4(),
                game_status=GameStatuses(1),
                game_participants=[player1, player2])

    list_of_games.append(game)
print(list_of_games)






