"""Scoring-math behaviour, pinned through the /score route."""


def test_upper_subtotal_sums_the_upper_section(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=5, twos=10, threes=15, fours=20, fives=12)  # = 62

    p1 = player(1)
    assert p1.subtotalupper == 62


def test_bonus_not_awarded_at_62(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=5, twos=10, threes=15, fours=20, fives=12)  # = 62

    p1 = player(1)
    assert p1.subtotalupper == 62
    assert p1.bonus == 0
    assert p1.total == 62


def test_bonus_awarded_at_63(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=5, twos=10, threes=15, fours=20, fives=13)  # = 63

    p1 = player(1)
    assert p1.subtotalupper == 63
    assert p1.bonus == 35
    assert p1.total == 63 + 35


def test_empty_categories_count_as_zero(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=5)  # everything else left blank

    p1 = player(1)
    assert p1.subtotalupper == 5
    assert p1.bonus == 0
    assert p1.total == 5


def test_total_includes_lower_section(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=5, threex=10, chance=7)

    p1 = player(1)
    # upper 5 (+0 bonus) + lower (10 + 7) = 22
    assert p1.subtotalupper == 5
    assert p1.total == 22
