import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
database_path = os.path.join("..", os.getenv("DB_PATH"))


class ItemCategory:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def get_titles(self):
        categories_titles = self.cursor.execute(
            "SELECT * FROM 'item category' "
        ).fetchall()
        return [title[-1] for title in categories_titles]  # Will return list of titles


ic = ItemCategory()
print(ic.get_titles())
