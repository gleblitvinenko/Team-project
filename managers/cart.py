import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
database_path = os.getenv("DB_PATH")


class Cart:
    def __init__(self):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def get_items_and_quantities_from_cart_by_telegram_id(self, telegram_id: int) -> dict[str, int]:
        items_and_quantities_list = self.cursor.execute(
            """
            SELECT "item".title, "cart item".quantity
            FROM "item"
            INNER JOIN "cart item"
            ON "cart item".item_id = "item".id
            INNER JOIN "cart"
            ON "cart item".cart_id = "cart".id
            INNER JOIN "user"
            ON "cart".user_id = "user".id
            WHERE "user".telegram_id = ?;
        """,
            (telegram_id,),
        ).fetchall()
        result_dict = {}
        for item_and_quantity in items_and_quantities_list:
            # ITEM NAME -> ITEM QUANTITY IN CART
            result_dict[item_and_quantity[0]] = item_and_quantity[1]
        return result_dict


if __name__ == "__main__":
    database_path = os.path.join("..", os.getenv("DB_PATH"))
    cart_manager = Cart()
    print(cart_manager.get_items_and_quantities_from_cart_by_telegram_id(531131340))
