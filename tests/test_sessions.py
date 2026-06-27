"""Each browser session owns its own game."""


def _start_game(client, names):
    data = {f"player{i + 1}": n for i, n in enumerate(names)}
    data["submit"] = "Let's play!"
    return client.post(f"/nametheplayers/{len(names)}", data=data)


def test_two_sessions_have_independent_games(app):
    c1 = app.test_client()
    c2 = app.test_client()

    _start_game(c1, ["Alice", "Bob"])
    _start_game(c2, ["Carol", "Dave"])

    page1 = c1.get("/score").get_data(as_text=True)
    page2 = c2.get("/score").get_data(as_text=True)

    assert "Alice" in page1 and "Carol" not in page1
    assert "Carol" in page2 and "Alice" not in page2


def test_score_without_a_game_redirects_home(client):
    resp = client.get("/score")
    assert resp.status_code == 302
    assert resp.headers["Location"] in ("/", "/index")


def test_game_can_be_joined_from_another_browser_by_code(app):
    from app.models import Game

    host = app.test_client()
    _start_game(host, ["Alice", "Bob"])
    code = Game.query.first().code
    assert code  # a code was generated

    visitor = app.test_client()           # a different browser, no cookie
    assert visitor.get("/score").status_code == 302   # can't see it yet

    visitor.get(f"/g/{code}")             # follow the shared link
    page = visitor.get("/score").get_data(as_text=True)
    assert "Alice" in page                # now in the same game


def test_join_code_is_case_insensitive(app):
    from app.models import Game

    host = app.test_client()
    _start_game(host, ["Alice", "Bob"])
    code = Game.query.first().code

    visitor = app.test_client()
    visitor.get(f"/g/{code.lower()}")
    assert "Alice" in visitor.get("/score").get_data(as_text=True)


def test_unknown_code_redirects_to_join(client):
    resp = client.get("/g/ZZZZ")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/join")


def test_reset_clears_only_this_session(app):
    c1 = app.test_client()
    c2 = app.test_client()
    _start_game(c1, ["Alice", "Bob"])
    _start_game(c2, ["Carol", "Dave"])

    c1.get("/reset")  # c1 abandons its game

    # c1 no longer has a game...
    assert c1.get("/score").status_code == 302
    # ...but c2's game is untouched.
    assert "Carol" in c2.get("/score").get_data(as_text=True)
