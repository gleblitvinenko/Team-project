import sqlite3


class User:

    def __init__(self, database_path: str) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def user_exists(self) -> bool:
        pass