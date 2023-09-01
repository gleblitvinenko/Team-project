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
                WHERE category.title = ?;
            """,
            (category_title,),
        ).fetchall()
        return [item_title[0] for item_title in item_titles]

    def get_item_details_dict_by_item_title(self, item_title: str) -> dict:
        item_details = self.cursor.execute(
            f"""
            SELECT *
            FROM "item"
            WHERE title = ?
            """,
            (item_title,),
        ).fetchall()
        return {
            "title": item_details[0][1],
            "id": item_details[0][2],
            "price": item_details[0][-1],
        }


# ----- TESTING OUTPUT ⬇️ -----
if __name__ == "__main__":
    database_path = os.path.join("..", os.getenv("DB_PATH"))
    item = Item()
    print(item.get_item_details_dict_by_item_title("Perfumery Item 1"))
