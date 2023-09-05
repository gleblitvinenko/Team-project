import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
database_path = os.getenv("DB_PATH")


class Cart:
    def __init__(self):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def get_items_and_quantities_from_cart_by_telegram_id(
        self, telegram_id: int
    ) -> list[dict]:
        items_prices_quantities_list = self.cursor.execute(
            """
            SELECT "item".title, "item".price, "cart item".quantity
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
        item_price_quantity_list_of_tuples = []
        for item_price_quantity_tuple in items_prices_quantities_list:
            temp_dict = {
                "title": item_price_quantity_tuple[0],
                "price": item_price_quantity_tuple[1],
                "quantity": item_price_quantity_tuple[2]
            }
            item_price_quantity_list_of_tuples.append(temp_dict.copy())
            temp_dict.clear()
        return item_price_quantity_list_of_tuples

    def get_user_id_by_telegram_id(self, telegram_id: int) -> int:
        user_id = self.cursor.execute(
            """
            SELECT id
            FROM "user"
            WHERE telegram_id = ?
            """, (telegram_id,)).fetchone()
        return user_id[0]

    def create_cart_for_user_by_telegram_id(self, telegram_id: int) -> None:
        """When user presses /start, cart is created"""

        if not self.is_cart_exists(telegram_id=telegram_id):

            user_id = self.get_user_id_by_telegram_id(telegram_id=telegram_id)
            self.cursor.execute(
                """
                INSERT INTO "cart" (user_id) VALUES (?)
                """, (user_id,)
            )
            self.connection.commit()

    def is_cart_exists(self, telegram_id: int) -> bool:
        """
        This method checks
        if cart exists
        to prevent UNIQUE constraint failed error,
        when creating cart for the first time
        """

        user_id = self.get_user_id_by_telegram_id(telegram_id=telegram_id)

        result = self.cursor.execute(
            """
            SELECT id
            FROM "cart"
            WHERE user_id = ?
            """, (user_id,)
        ).fetchone()

        return bool(result)

    def get_cart_id_by_user_id(self, telegram_id) -> int:

        if self.is_cart_exists(telegram_id=telegram_id):
            user_id = self.get_user_id_by_telegram_id(telegram_id=telegram_id)
            cart_id = self.cursor.execute(
                """
                SELECT id
                FROM cart
                WHERE user_id = ?
                """, (user_id,)
            ).fetchone()
            return cart_id[0]

    def add_item_and_quantity_to_user_cart(
        self, item_title: str, item_quantity: int, telegram_id: int
    ) -> None:
        """ Method that adds items to the user cart"""
        user_id = self.get_user_id_by_telegram_id(telegram_id=telegram_id)
        cart_id = self.get_cart_id_by_user_id(telegram_id=telegram_id)
        # TODO if items already in cart -> just change quantity | else -> add in cart
        self.cursor.execute(
            """

            """
        )


if __name__ == "__main__":
    database_path = os.path.join("..", os.getenv("DB_PATH"))
    cart_manager = Cart()
    # print(cart_manager.get_items_and_quantities_from_cart_by_telegram_id(531131340))
    # cart_manager.get_user_id_by_telegram_id(531131340)
    # cart_manager.create_cart_for_user_by_telegram_id(531131340)
    # print(cart_manager.is_cart_exists(531131340))
    # print(cart_manager.get_cart_id_by_user_id(531131340))
