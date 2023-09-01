import os.path
import sqlite3
from dotenv import load_dotenv

load_dotenv()
database_path = os.getenv("DB_PATH")


class Item:
    def __init__(self):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def get_items_titles_list_by_category_title(self, category_title: str) -> list[str]:
        item_titles = self.cursor.execute(
            f"""SELECT item.title
                FROM "item"
                INNER JOIN "item category" AS category
                ON item.category = category.id
                WHERE category.title = '{category_title}';
            """).fetchall()
        return [item_title[0] for item_title in item_titles]
