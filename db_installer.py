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
    "item_id" INTEGER NOT NULL UNIQUE,
    "category" INTEGER,
    "price" DECIMAL,
    FOREIGN KEY ("category") REFERENCES "item category" ("id")
    )
"""


def create_db() -> None:
    with sqlite3.connect("cosmetics_shop.db") as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_USER_TABLE)
        cursor.execute(CREATE_ITEM_CATEGORY_TABLE)
        cursor.execute(CREATE_ITEM_TABLE)
        connection.commit()


if __name__ == "__main__":
    create_db()
