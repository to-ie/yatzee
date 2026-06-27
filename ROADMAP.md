# Yahtzee score-card — improvement roadmap

Tracking improvements to the app. Checked items are done; the rest are
ordered roughly by leverage.

---

## ✅ Done

### Responsive design overhaul
- Added the missing `<meta name="viewport">` — this was the root cause of the
  desktop layout breaking (mobile browsers were auto-shrinking a fixed ~980px
  mockup; desktop had no such shrink).
- Rewrote `style.css` from fixed pixels to mobile-first fluid CSS: `clamp()`
  type, flexbox/grid instead of floats, CSS variables, a centered
  `max-width` container, and a breakpoint at 640px (Upper/Lower stack on
  mobile, side-by-side on desktop).
- Verified in a real browser at 390px and 1280px widths.

### Quick wins
- Self-hosted the Lato / Lilita One fonts under `static/fonts/` (works
  offline; no Google Fonts dependency).
- Removed `systemd-python` from `requirements.txt` so
  `pip install -r requirements.txt` works on macOS/Windows.
- Added `.gitignore` and untracked `venv/`, `__pycache__/`, and `app.db`
  (~2700 files that shouldn't have been committed).
- Added `alt` text to every template image (a11y).
- Winner highlight on the end screen (🏆 + highlighted row).
- Fixed unbalanced `<div>`s in the bonus block and a stray literal `.` in
  `score.html`.
- Decoupled `end.html` from the `col1`/`col2`/`row-*` classes it was sharing
  (with conflicting meaning) with the scorecard.

### Test safety net (pre-refactor)
- Added `tests/` (pytest) — black-box integration tests through the routes
  covering the scoring math (subtotal, bonus boundary at 62/63, empty = 0,
  lower section) and game flow (turn rotation + wrap, full detection,
  redirect to `/end`). 10 tests, all green.
- `requirements-dev.txt` pins `pytest`. Run with `python -m pytest`.
- Discovered behaviour to preserve/fix in the refactor: **a score submit
  overwrites the player's entire sheet**, so the app depends on the GET
  request pre-filling the form to round-trip prior values. The refactor
  should store per-category and update only what changed.

### Data model refactor
- Replaced the hardcoded `playerone…playerfive` columns and the `Score` table
  of 13 `String(64)` columns with a proper `Game ──< Player` relationship;
  category scores are now **nullable integers** (NULL = unfilled).
- `subtotalupper` / `bonus` / `total` / `full` are **computed properties**, so
  totals are always current — this fixed the long-standing "totals don't
  update in real time" bug (verified: an opponent's total shows live on
  another player's turn).
- Routes and templates iterate `CATEGORIES` / `game.players` instead of
  repeating 13 fields and 5 players — `routes.py` dropped from ~280 to ~115
  lines; the `score()`/`end()` per-player queries and the 4-branch
  end-of-game check are gone.
- Removed dead code (unreachable `return` in `numberplayers()`, the
  meaningless `/pause` logic). Added the Alembic migration
  `0490a4803d3a_refactor_to_game_player_model`; the full `flask db upgrade`
  path was verified on a clean database.
- All 10 behaviour tests still pass.

### Server-side score validation
- Score fields are now validated `IntegerField`s, so non-numeric input is a
  friendly form error instead of a 500. Per-category rules: upper section
  bounded by `face*5` and a multiple of the face; three/four-of-a-kind and
  chance `0..30`; full house `0/25`; straights `0/30` and `0/40`; yahtzee
  `0/50`; blank = unfilled; `0` = a valid scratch.
- Invalid submits re-render with per-field error messages and a flash banner,
  and do **not** save or advance the turn.
- Added `tests/test_validation.py` (7 tests). Full suite: 17 passing.

### Hardening & hygiene
- Fixed the "overwrite whole sheet" footgun: a submit now only writes
  categories that were filled in, so a blank box can't wipe a score entered
  on an earlier turn (no longer relies on the GET pre-fill for integrity).
  Pinned by a regression test. Full suite: **18 passing**.
- Removed the hardcoded `SECRET_KEY` from source — it now comes from the
  environment, with a random per-process fallback for local dev.
- The flash-message markup in `base.html` is now actually used (validation
  errors), and styled.
- Documented `python -m pytest` and the `SECRET_KEY` / `DATABASE_URL`
  environment variables in the README.

---

## 💡 Ideas / nice-to-haves

### Gameplay / UX
- Show each player's running total live on the scorecard, not just the bottom
  panel; highlight whose turn it is.
- One-tap value buttons / auto-suggest for fixed categories (full house = 25,
  yahtzee = 50, straights) — faster entry, fewer typos.
- Explicit "scratch / zero" button per category.
- Undo last entry.
- Stronger confirmation before `/reset` (it wipes the whole game).

### Multi-game / multi-user
- Multiple concurrent games via Flask `session` + a game id (today everything
  is a single global `Game` with `id=1` — a second browser collides).
- Simple auth (magic-link / email-less).
- Per-player history & stats (high scores, averages).

### Polish
- Favicon + PWA manifest (add-to-home-screen; the app is already phone-shaped).
- `prefers-reduced-motion` and form `<label>`s for accessibility.
- Export/import games as CSV/JSON.
