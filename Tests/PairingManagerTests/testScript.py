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

    # TODO: ten interfejs jest nieodporny na zmiany - powinieneś przyjmować obiek ScoreBase albo WTCScore jako input do funkcji typu edit
    # TODO wyszukiwanie gier po indexach listy to też zła droga na tym poziomie
    # TODO w ogóle Tournament powinien mieć metody do manipulowania grami, a nie zwracać gry i na nich pracować - to jest trochę niebezpieczne, ktoś może zrobić kopię obiektu przez przypadek
    # TODO tak by to moglo wyglądać:
    #  pl1_score = WTCScore()
    #  pl2_score = WTCScore()
    #  T.GetGame(game_id).edit_score(pl1_score, pl2_score)
    #  albo:
    #  T.EditGame(game_id, pl1_score, pl2_score)

    games[0].edit_players_score(pl1_points=8, pl1_tiebreakers=55, pl2_points=12, pl2_tiebreakers=65)
    games[1].edit_players_score(pl1_points=15, pl1_tiebreakers=75, pl2_points=5, pl2_tiebreakers=65)

    # or using update_players_score
    # TODO tak jak tutaj jest lepiej, tylko trcohe wiecej abstrakcji typu WTCScore, poprzedniej wersji by nie pokazywał jako przykład
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
    print(t.set_pairing_manager(Tournament.PairingEnum.Swiss))  # TODO zamiast nazwyać to PairingEnum to nazwij to PairingTypes i patrz jak ładnie jest wykorzystane: Tournament.ParingTypes.Swiss




