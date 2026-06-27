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

---

## 🔜 Next up

### 1. Data model refactor (highest leverage)
Replace the hardcoded `playerone…playerfive` columns and 13 `String(64)`
score columns with proper relations:

```
Game ──< Player ──< Score   (category enum, integer value, NULL = unfilled)
```

This collapses ~200 lines of repeated routes/templates into loops and is the
prerequisite for most other improvements. See `models.py`, and the repeated
queries in `routes.py` (`score()` / `end()`).

### 2. Correctness / bug fixes
- **Server-side score validation** — score fields are free-text `StringField`s
  parsed with `int(float(...))`; any non-numeric input is an instant 500.
- **Real-time totals** — each player's total is only recomputed on their own
  turn, so the scoreboard always lags (the `TODO` in `routes.py`).
- **Unambiguous "filled"** — a scratched 0 is currently indistinguishable from
  unfilled (fixed naturally by the nullable-integer model above).
- Remove dead code: unreachable `return` in `numberplayers()`, the
  meaningless `nextplayer = 3` in `/pause`.

### 3. Engineering hygiene
- Real `SECRET_KEY` (drop the hardcoded fallback in `config.py`).
- `pytest` suite around the scoring math (bonus, totals, end-of-game) — makes
  the model refactor safe.
- Regenerate the broken bundled `venv` (or just rely on the documented setup).
- Wire up or remove the unused flash-message markup in `base.html`.

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
