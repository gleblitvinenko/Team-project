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

    def check_field(self, telegram_id: int, field: str) -> bool:
        result = self.cursor.execute(
            f"SELECT {field} FROM user WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        print(result)
        return result[0] is not None

    def create_user(self, telegram_id: int) -> None:
        self.cursor.execute("INSERT INTO user (telegram_id) VALUES (?)", (telegram_id,))
        self.connection.commit()

    def update_profile(self, telegram_id: int, **kwargs) -> None:
        for key, value in kwargs.items():
            self.cursor.execute(
                f"UPDATE user SET {key} = ? WHERE telegram_id = ?", (value, telegram_id)
            )
        self.connection.commit()

    def __del__(self):
        self.connection.close()
