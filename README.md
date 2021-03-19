# PairingLibrary

How to use:

Creating the tournament.
Simply create a tournament object. 

```
from PairingLibrary.Tournament import Tournament
t = Tournament()
```


To register the player use Tournament’s register_player method() It takes one mandatory argument which is the name. You can also fill the nickname and choose the ScoringClass. Default implementation is WTCScoreSystem used in Warhammer 40k games. 

```
t.register_player(name='Johnny Bravo', nickname='The Handsome')
t.register_player(name='Buzz Lightyear', nickname='Space Ranger')
t.register_player(name='Woody Pride', nickname='The Sheriff')
t.register_player(name='Uncle Beans', nickname='The chief')
```


To create a new round use create_round() It returns the Round object which contains information about pairings, players and their score. 
```
t.create_round()
>>> Round(id=None, round_id=UUID('35299d13-1d3d-40ab-8cea-45304a6333f6'), ts_start=1616148762.511553, ts_end=None, round_status=<RoundStatuses.Ongoing: 'Ongoing'>, games_in_round=[Game(game_id=UUID('ebe30fd6-82eb-4586-89e6-9bb57e212084'), game_status=<GameStatuses.Ongoing: 'Ongoing'>, game_participants=[(Woody 'The Sheriff' Pride, Points: 0, tiebreakers: 0), (Buzz 'Space Ranger' Lightyear, Points: 0, tiebreakers: 0)]), Game(game_id=UUID('7a3bd93d-58c1-4189-b663-618e1d9d3dda'), game_status=<GameStatuses.Ongoing: 'Ongoing'>, game_participants=[(Johnny 'The Handsome' Bravo, Points: 0, tiebreakers: 0), (Uncle 'The chief' Beans, Points: 0, tiebreakers: 0)])])
```

To get all games in the round
```
t.show_games_in_the_round()
>>> [Game(game_id=UUID('21593177-53da-4fa8-a996-b80ff46e6594'), game_status=<GameStatuses.Ongoing: 'Ongoing'>, game_participants=[(Woody 'The Sheriff' Pride, Points: 0, tiebreakers: 0), (Johnny 'The Handsome' Bravo, Points: 0, tiebreakers: 0)]), Game(game_id=UUID('243d1cb2-e8d3-40bc-83e1-3dd23c71bb63'), game_status=<GameStatuses.Ongoing: 'Ongoing'>, game_participants=[(Buzz 'Space Ranger' Lightyear, Points: 0, tiebreakers: 0), (Uncle 'The chief' Beans, Points: 0, tiebreakers: 0)])
```


Player score edition. This method modifies the current score. It has no effect on the total score until the round is finished
```
t.update_players_score(game_id='4e468fe9-5599-45cd-95f0-9918e13bf376', pl1_points=8, pl1_tiebreakers=55,
                      pl2_points=12, pl2_tiebreakers=65)
```


To get the list of all the players in the Round use show_players(). It returns the list of Player objects.
```
players = t.show_players()
>>> [Woody Pride, Uncle Beans, Johnny Bravo, Buzz Lightyear
```

To end round use finish_round(). It returns the finished round object, modify total score, set timestamps and change round and game statuses to finish. 
```
t.finish_round()
>>>Round(id=None, round_id=UUID('f472061b-6959-4b96-a66c-879f59b7841b'), ts_start=1616147874.191851, ts_end=1616147874.191851, round_status=<RoundStatuses.Finished: 'Finished'>, games_in_round=[Game(game_id=UUID('1fdc8bef-e9c4-4dfb-b957-1a0eb7b412dd'), game_status=<GameStatuses.Finished: 'Finished'>, game_participants=[(Buzz 'Space Ranger' Lightyear, Points: 8, tiebreakers: 55), (Woody 'The Sheriff' Pride, Points: 12, tiebreakers: 65)]), Game(game_id=UUID('c92898bd-5a8d-48a8-8e3a-148fb79c79e3'), game_status=<GameStatuses.Finished: 'Finished'>, game_participants=[(Johnny 'The Handsome' Bravo, Points: 15, tiebreakers: 75), (Uncle 'The chief' Beans, Points: 5, tiebreakers: 65)])])
```


You can also get the current total score of players with
```
t.show_results()
>>>[(Johnny 'The Handsome' Bravo, Points: 5, tiebreakers: 65), (Buzz 'Space Ranger' Lightyear, Points: 15, tiebreakers: 75), (Woody 'The Sheriff' Pride, Points: 12, tiebreakers: 65), (Uncle 'The chief' Beans, Points: 8, tiebreakers: 55)]
```

Before generating next round you can change pairing manager with set_pairing_manager(). It returns the name of the PairingManager class in use. 
```
t.set_pairing_manager(Tournament.PairingEnum.Swiss)
>>> SwissPairingManager
```







