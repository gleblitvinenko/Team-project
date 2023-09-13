import os.path

from managers.manager import Manager


class Item(Manager):
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

    def get_item_id_by_title(self, title: str) -> int:
        item_id = self.cursor.execute(
            """
            SELECT item_id
            FROM item
            WHERE title = ?
            """,
            (title,),
        ).fetchone()[0]

        return item_id


# ----- TESTING OUTPUT ⬇️ -----
if __name__ == "__main__":
    item = Item()
    item.database_path = os.path.join("..", os.getenv("DB_PATH"))
    # print(item.get_item_details_dict_by_item_title("Perfumery Item 1"))
    print(item.get_item_id_by_title("Perfumery Item 1"))
