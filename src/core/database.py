"""Persistent user store backed by a local SQLite database."""

import json
import sqlite3
from pathlib import Path

# battleship.db lives at the project root (one level above src/)
_DB_PATH = Path(__file__).resolve().parent.parent.parent / "battleship.db"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(str(_DB_PATH))


def init_db() -> None:
    """Create required tables if they do not exist yet."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL UNIQUE,
                last_played TEXT    NOT NULL DEFAULT (datetime('now')),
                rating      INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        # Try adding rating column for existing databases backwards compatibility
        try:
            conn.execute("ALTER TABLE users ADD COLUMN rating INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS game_states (
                username   TEXT PRIMARY KEY,
                game_data  TEXT NOT NULL,
                saved_at   TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY(username) REFERENCES users(name)
            )
            """
        )
        conn.commit()


def get_recent_users(limit: int = 10) -> list:
    """Return up to *limit* user names ordered by most recently played."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT name FROM users ORDER BY last_played DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [row[0] for row in rows]


def upsert_user(name: str) -> None:
    """Insert a new user or update the last_played timestamp for an existing one."""
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (name, last_played, rating)
            VALUES (?, datetime('now'), 0)
            ON CONFLICT(name) DO UPDATE SET last_played = datetime('now')
            """,
            (name,),
        )
        conn.commit()


def get_user_rating(name: str) -> int:
    """Return the database rating for the user (default 0)."""
    with _connect() as conn:
        row = conn.execute("SELECT rating FROM users WHERE name = ?", (name,)).fetchone()
    if row:
        return row[0]
    return 0


def update_user_rating(name: str, delta: int) -> None:
    """Apply a rating delta to an existing user."""
    with _connect() as conn:
        conn.execute("UPDATE users SET rating = rating + ? WHERE name = ?", (delta, name))
        conn.commit()


def has_game_state(username: str) -> bool:
    """Return True when a saved game exists for *username*."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM game_states WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone()
    return row is not None


def save_game_state(username: str, game_snapshot: dict) -> None:
    """Persist a serialized game snapshot for *username*."""
    payload = json.dumps(game_snapshot, separators=(",", ":"))
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO game_states (username, game_data, saved_at)
            VALUES (?, ?, datetime('now'))
            ON CONFLICT(username) DO UPDATE SET
                game_data = excluded.game_data,
                saved_at = datetime('now')
            """,
            (username, payload),
        )
        conn.commit()


def load_game_state(username: str) -> dict | None:
    """Load and deserialize the saved game snapshot for *username*."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT game_data FROM game_states WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return None

    try:
        data = json.loads(row[0])
    except (json.JSONDecodeError, TypeError):
        return None

    return data if isinstance(data, dict) else None


def delete_game_state(username: str) -> None:
    """Delete the saved game snapshot for *username*."""
    with _connect() as conn:
        conn.execute("DELETE FROM game_states WHERE username = ?", (username,))
        conn.commit()
