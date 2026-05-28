import sqlite3
import io
import numpy as np
from PIL import Image


DB_PATH = "face_recognition.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS images (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                data    BLOB NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS embeddings (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                vector  BLOB NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


def create_user(name: str, conn: sqlite3.Connection) -> int:
    cur = conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    return cur.lastrowid


def save_face(user_id: int, image: Image.Image, embedding: np.ndarray, conn: sqlite3.Connection):
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    conn.execute(
        "INSERT INTO images (user_id, data) VALUES (?, ?)",
        (user_id, buf.getvalue()),
    )
    conn.execute(
        "INSERT INTO embeddings (user_id, vector) VALUES (?, ?)",
        (user_id, embedding.tobytes()),
    )


def load_all_embeddings() -> dict[str, np.ndarray]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT users.name, embeddings.vector
            FROM users JOIN embeddings ON users.id = embeddings.user_id
        """).fetchall()

    result = {}
    for name, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        result[name] = vec
    return result


def delete_user(name: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()
        if row is None:
            return False
        uid = row[0]
        conn.execute("DELETE FROM images     WHERE user_id = ?", (uid,))
        conn.execute("DELETE FROM embeddings WHERE user_id = ?", (uid,))
        conn.execute("DELETE FROM users      WHERE id      = ?", (uid,))
    return True
