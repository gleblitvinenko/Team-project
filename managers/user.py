import os

from managers.manager import Manager


class User(Manager):
    def user_exists(self, telegram_id: int) -> bool:
        result = self.cursor.execute(
            "SELECT telegram_id FROM user WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        return result is not None

    def check_field(self, telegram_id: int, field: str) -> bool:
        result = self.cursor.execute(
            f"SELECT {field} FROM user WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
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

    def get_info_for_profile(self, telegram_id: int) -> dict[str, str]:
        result = self.cursor.execute(
            f"""SELECT first_name, last_name, phone_number, reg_date
                FROM user
                WHERE telegram_id = ?
            """,
            (telegram_id,),
        ).fetchone()
        return {
            "first_name": result[0],
            "last_name": result[1],
            "phone_number": result[2],
            "reg_date": result[3],
        }

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    user_manager = User()
    user_manager.database_path = os.path.join("..", os.getenv("DB_PATH"))
    print(user_manager.get_info_for_profile(telegram_id=531131340))
