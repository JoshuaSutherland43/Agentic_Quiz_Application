import sqlite3
import json
import os

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "questions.json")
DB_PATH = os.path.join(os.path.dirname(__file__), "history.db")


class QuizDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS highscore (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            score INTEGER
        )""")
        self.conn.commit()

    def load_questions(self):
        with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_attempt(self, score):
        c = self.conn.cursor()
        c.execute("INSERT INTO stats (score) VALUES (?)", (score,))
        self.conn.commit()

    def get_attempts(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM stats")
        return c.fetchone()[0]

    def get_high_score(self):
        c = self.conn.cursor()
        c.execute("SELECT score FROM highscore WHERE id=1")
        row = c.fetchone()
        return row[0] if row else 0

    def save_high_score(self, score):
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO highscore (id, score) VALUES (1, ?)", (score,)
        )
        self.conn.commit()
