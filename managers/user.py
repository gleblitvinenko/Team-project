import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
database_path = os.path.join("..", os.getenv("DB_PATH"))


class User:
    def __init__(self, telegram_id) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

        if not self.user_exists(telegram_id):
            self.cursor.execute(
                "INSERT INTO user (telegram_id) VALUES (?)", (telegram_id,)
            )
            self.connection.commit()

    def user_exists(self, telegram_id: int) -> bool:
        self.cursor.execute("SELECT * FROM user WHERE telegram_id=?", (telegram_id,))
        return len(list(self.cursor)) != 0
