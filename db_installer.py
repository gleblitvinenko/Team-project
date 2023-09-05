import sqlite3

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS "user" (
        "id" INTEGER NOT NULL,
        "telegram_id" INTEGER NOT NULL UNIQUE ,
        "phone_number" VARCHAR NULL,
        "reg_date" DATE DEFAULT (date('now')),
        "is_admin" BOOLEAN DEFAULT 0,
        "first_name" VARCHAR NULL,
        "last_name" VARCHAR NULL,
        PRIMARY KEY("id")
    )
"""


CREATE_ITEM_CATEGORY_TABLE = """
    CREATE TABLE IF NOT EXISTS "item category" (
    "id" INTEGER PRIMARY KEY,
    "title" VARCHAR UNIQUE
    )
"""


CREATE_ITEM_TABLE = """
    CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY,
    "title" VARCHAR,
    "item_id" INTEGER NOT NULL UNIQUE,
    "category" INTEGER,
    "price" DECIMAL,
    FOREIGN KEY ("category") REFERENCES "item category" ("id")
    )
"""

CREATE_CART_TABLE = """
    CREATE TABLE IF NOT EXISTS "cart" (
    "id" INTEGER PRIMARY KEY,
    "user_id" INTEGER UNIQUE,
    FOREIGN KEY (user_id) REFERENCES user(id)
    )
"""

CREATE_CART_ITEM_TABLE = """
    CREATE TABLE IF NOT EXISTS "cart item" (
    "id" INTEGER PRIMARY KEY,
    "cart_id" INTEGER,
    "item_id" INTEGER,
    "quantity" INTEGER,
    FOREIGN KEY (cart_id) REFERENCES cart(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
    )
"""

TABLES_TO_CREATE = [
    CREATE_USER_TABLE,
    CREATE_ITEM_CATEGORY_TABLE,
    CREATE_ITEM_TABLE,
    CREATE_CART_TABLE,
    CREATE_CART_ITEM_TABLE,
]


def create_db() -> None:
    with sqlite3.connect("cosmetics_shop.db") as connection:
        cursor = connection.cursor()
        for table in TABLES_TO_CREATE:
            cursor.execute(table)
        connection.commit()


if __name__ == "__main__":
    create_db()
