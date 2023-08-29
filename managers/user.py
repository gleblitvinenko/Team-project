import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
database_path = os.getenv("DB_PATH")


class User:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def user_exists(self, telegram_id: int) -> bool:
        result = self.cursor.execute(
            "SELECT telegram_id FROM user WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        return result is not None

    def create_user(self, telegram_id: int) -> None:
        self.cursor.execute("INSERT INTO user (telegram_id) VALUES (?)", (telegram_id,))
        self.connection.commit()

    def __del__(self):
        self.connection.close()
