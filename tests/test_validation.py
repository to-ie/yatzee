"""Server-side score validation: bad input is rejected, not saved, no 500."""


def test_non_numeric_input_does_not_crash(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    resp = score_turn(ones="banana")

    assert resp.status_code == 200          # re-renders the form, not a 500
    assert player(1).ones is None           # nothing was saved


def test_invalid_score_does_not_advance_the_turn(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones="banana")               # rejected
    score_turn(ones=4)                       # still Alice's turn

    assert player(1).ones == 4
    assert player(2).ones is None


def test_upper_score_out_of_range_is_rejected(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(ones=9)                       # max for ones is 5

    assert player(1).ones is None


def test_upper_score_must_be_a_multiple_of_the_face(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(twos=7)                        # twos must be a multiple of 2

    assert player(1).twos is None


def test_fixed_category_rejects_arbitrary_value(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(fullhouse=10)                  # full house is 0 or 25

    assert player(1).fullhouse is None


def test_fixed_category_accepts_canonical_value(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(fullhouse=25)

    assert player(1).fullhouse == 25


def test_zero_is_a_valid_scratch(make_game, score_turn, player):
    make_game(["Alice", "Bob"])
    score_turn(yahtzee=0)                     # scratching the category

    assert player(1).yahtzee == 0
