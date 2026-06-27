"""Turn rotation and end-of-game behaviour, pinned through the routes."""


def test_turn_advances_to_next_player(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=3)  # Alice's turn (playerid 1)

    # Alice's score is recorded; Bob's is still untouched.
    assert player(1).subtotalupper == 3
    assert player(2).subtotalupper == 0


def test_turn_wraps_back_to_first_player(make_game, score_turn, player):
    # Each submit is tagged in `chance` so we can see whose row it landed on.
    # (Note: a submit overwrites the player's whole sheet, so we use distinct
    # markers rather than accumulating values across turns.)
    make_game(["Alice", "Bob"])
    score_turn(chance=11)  # turn 1 -> Alice
    score_turn(chance=22)  # turn 2 -> Bob
    score_turn(chance=33)  # turn 3 -> should wrap back to Alice

    assert player(1).chance == 33   # third turn landed on Alice
    assert player(2).chance == 22   # Bob untouched since his turn


def test_player_marked_full_when_all_categories_entered(
    make_game, score_turn, player, full_sheet
):
    make_game(["Alice", "Bob"])
    score_turn(**full_sheet)

    assert player(1).full is True


def test_player_not_full_with_an_empty_category(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=1)  # only one category filled

    assert player(1).full is False


def test_game_redirects_to_end_when_everyone_is_full(
    make_game, score_turn, client, full_sheet
):
    make_game(["Alice", "Bob"])
    score_turn(**full_sheet)  # Alice complete -> turn passes to Bob
    score_turn(**full_sheet)  # Bob complete

    resp = client.get("/score")
    assert resp.status_code == 302
    assert "/end" in resp.headers["Location"]
