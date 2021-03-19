from PairingLibrary.Tournament import Tournament

if __name__ == '__main__':

    # to create a tournament
    t = Tournament()

    # to register players
    t.register_player(name='Johnny Bravo', nickname='The Handsome')
    t.register_player(name='Buzz Lightyear', nickname='Space Ranger')
    t.register_player(name='Woody Pride', nickname='The Sheriff')
    t.register_player(name='Uncle Beans', nickname='The chief')

    # to create a round
    round1 = t.create_round()

    # to get all games in the round
    print(t.show_games_in_the_round())


    # # Score edition from the game object
    games = t.show_games_in_the_round()

    games[0].edit_players_score(pl1_points=8, pl1_tiebreakers=55, pl2_points=12, pl2_tiebreakers=65)
    games[1].edit_players_score(pl1_points=15, pl1_tiebreakers=75, pl2_points=5, pl2_tiebreakers=65)

    # or using update_players_score
    t.update_players_score(game_id=games[0].game_id, pl1_points=8, pl1_tiebreakers=55,
                           pl2_points=12, pl2_tiebreakers=65)
    t.update_players_score(game_id=games[1].game_id, pl1_points=15, pl1_tiebreakers=75, pl2_points=5, pl2_tiebreakers=65
                           )

    # To get the players in the current round use
    print(t.show_players_in_the_round())

    # Ending the round also return the results.
    print(t.end_round())

    # to watch the reuslts
    print(t.show_results())

    # to create the next round
    round2 = t.create_round()

    # to change the pairing manager
    print(t.set_pairing_manager(Tournament.PairingEnum.Swiss))




