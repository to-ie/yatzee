# Yatzee

A quick-and-dirty **Flask** app for keeping **Yatzee/Yahtzee** scores at the table. Currently **single-user** only (one active browser/session at a time).

> Project started on **2023‑05‑13**. Licensed under **GPL‑3.0**.

---

## Features

* Fast score entry for the 13 standard categories
* Simple totals and upper‑section bonus calculation
* Persists scores in a local SQLite database

> Note: This is intentionally minimal—perfect for a pub game night or as a Flask learning project.

---

## Tech stack

* **Python** (3.10+ recommended)
* **Flask** (with Jinja templates)
* **SQLite** (via SQLAlchemy)
* **Flask‑Migrate** for schema migrations

---

## Getting started

### 1) Clone and set up a virtualenv

```bash
git clone https://github.com/to-ie/yatzee
cd yatzee
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment

Set the Flask entrypoint and enable dev mode (optional):

```bash
export FLASK_APP=yatzee.py
export FLASK_ENV=development   # optional: enables auto‑reload & debug
```

### 3) Initialize / upgrade the database

Migrations are included. Apply them to create `app.db`:

```bash
flask db upgrade
```

If you’re starting fresh without the `migrations/` folder for any reason, you can rebuild:

```bash
flask db init
flask db migrate -m "initial tables"
flask db upgrade
```

### 4) Run the app

```bash
flask run
# or
python yatzee.py
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## Usage

* Create a new game and enter scores after each roll.
* The app sums upper/lower sections and applies the standard **+35 bonus** when the upper section >= 63.
* One user/session at a time; multiple devices will collide.

> Tip: If you want to clear all data, stop the app and delete `app.db`.

---

## Screenshots


<img width="527" height="960" alt="image" src="https://github.com/user-attachments/assets/fbe7d22b-18ef-48eb-8a03-f07063a1ae83" />
<img width="713" height="1600" alt="image" src="https://github.com/user-attachments/assets/39d38182-3bad-484a-9e72-897f8a40f59b" />



---

## Development

* Code lives under `app/` with templates and routes.
* Configuration lives in `config.py`.
* Database migrations are in `migrations/`.

### Running formatters/tests

(If you add tooling later, e.g. `ruff`/`black`/`pytest`, document the commands here.)

---

## Deployment (basic)

For a tiny self‑host:

```bash
pip install gunicorn
export FLASK_APP=yatzee.py
gunicorn -w 2 -b 0.0.0.0:8000 yatzee:app
```

Put a reverse proxy (Nginx/Caddy) in front if exposing to the internet.

---

## Roadmap / ideas

* Multi‑user with simple auth (email‑less or magic‑link)
* Multiple concurrent tables/games
* Per‑player history & stats (high scores, averages)
* Mobile‑first UI polish and PWA install
* Export/import games as CSV/JSON

Contributions and PRs welcome.

---

## License

This project is released under the **GPL‑3.0** license.

