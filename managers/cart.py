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
        """
        This method gets
        item title, item price, item quantity, item_id in the cart
        for example, to visualize these data in user cart section
        """

        items_prices_quantities_list = self.cursor.execute(
            """
            SELECT "item".title, "item".price, "cart item".quantity, "item".item_id
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
        item_price_quantity_list_of_dicts = []
        for item_price_quantity_tuple in items_prices_quantities_list:
            temp_dict = {
                "title": item_price_quantity_tuple[0],
                "price": item_price_quantity_tuple[1],
                "quantity": item_price_quantity_tuple[2],
                "item_id": item_price_quantity_tuple[3],
            }
            item_price_quantity_list_of_dicts.append(temp_dict.copy())
            temp_dict.clear()
        return item_price_quantity_list_of_dicts

    def get_user_id_by_telegram_id(self, telegram_id: int) -> int:
        """
        This method gets user id
        by telegram_id
        """

        user_id = self.cursor.execute(
            """
            SELECT id
            FROM "user"
            WHERE telegram_id = ?
            """,
            (telegram_id,),
        ).fetchone()

        if user_id is not None:
            return user_id[0]

    def create_cart_for_user_by_telegram_id(self, telegram_id: int) -> None:
        """
        When user presses /start,
        cart is created
        """

        if not self.is_cart_exists(telegram_id=telegram_id):
            user_id = self.get_user_id_by_telegram_id(telegram_id=telegram_id)
            self.cursor.execute(
                """
                INSERT INTO "cart" (user_id) VALUES (?)
                """,
                (user_id,),
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
            """,
            (user_id,),
        ).fetchone()

        return bool(result)

    def is_item_in_cart_already_exists(self, cart_id: int, item_id: int) -> bool:
        """
        This method checks
        if such items exist in current cart
        """
        cart_item_id = self.cursor.execute(
            """
            SELECT item_id
            FROM "cart item"
            WHERE cart_id = ? AND item_id = ?
            """,
            (cart_id, item_id),
        ).fetchone()

        return bool(cart_item_id)

    def get_item_id_by_item_title(self, item_title: str) -> int:
        """
        This method gets item id
        by item title
        """
        item_id = self.cursor.execute(
            """
            SELECT id
            FROM "item"
            WHERE title = ? 
            """,
            (item_title,),
        ).fetchone()

        if item_id is not None:
            return item_id[0]

    def get_item_quantity_or_none(
        self, telegram_id: int, item_title: str
    ) -> int | None:
        """
        This method checks
        if item quantity
        in "cart item" table
        equals not zero.
        """

        cart_id = self.get_cart_id_by_user_id(telegram_id=telegram_id)
        item_id = self.get_item_id_by_item_title(item_title=item_title)

        item_quantity = self.cursor.execute(
            """
            SELECT quantity
            FROM "cart item"
            WHERE cart_id = ? AND item_id = ?
            """,
            (cart_id, item_id),
        ).fetchone()

        if item_quantity is not None:
            return item_quantity[0]

    def get_cart_id_by_user_id(self, telegram_id: int) -> int | None:
        """
        Method that returns
        cart id by user id
        """
        if self.is_cart_exists(telegram_id=telegram_id):
            user_id = self.get_user_id_by_telegram_id(telegram_id=telegram_id)
            cart_id = self.cursor.execute(
                """
                SELECT id
                FROM "cart"
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if cart_id is not None:
                return cart_id[0]

    def add_item_and_quantity_to_user_cart(
        self, item_title: str, item_quantity: int, telegram_id: int
    ) -> None:
        """
        Method that adds items
        to the user cart
        or change their quantity
        if they exist
        """

        cart_id = self.get_cart_id_by_user_id(telegram_id=telegram_id)
        item_id = self.get_item_id_by_item_title(item_title=item_title)

        if item_id is None:
            # If by some miracle a non-existent product is got
            return

        item_quantity_in_table = self.get_item_quantity_or_none(
            telegram_id=telegram_id, item_title=item_title
        )

        try:
            if item_quantity_in_table >= 0:
                # UPDATE ITEM QUANTITY
                self.cursor.execute(
                    """
                    UPDATE "cart item"
                    SET quantity = ?
                    WHERE cart_id = ? and item_id = ?
                    """,
                    (item_quantity_in_table + item_quantity, cart_id, item_id),
                )
        except TypeError:
            # CREATING RECORD
            self.cursor.execute(
                """
                INSERT INTO "cart item" (cart_id, item_id, quantity)
                VALUES (?, ?, ?)

                """,
                (cart_id, item_id, item_quantity),
            )
        finally:
            self.connection.commit()


# ⬇️ TEST STAFF ⬇️
if __name__ == "__main__":
    database_path = os.path.join("..", os.getenv("DB_PATH"))
    cart_manager = Cart()
