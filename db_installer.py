import sqlite3

CREATE_USER_TABLE = """
    CREATE TABLE "user" (
        "id" INTEGER NOT NULL,
        "telegram_id" INTEGER NOT NULL,
        "phone_number" VARCHAR NULL,
        "reg_date" DATE DEFAULT (date('now')),
        "is_admin" BOOLEAN DEFAULT 0,
        "first_name" VARCHAR NULL,
        "last_name" VARCHAR NULL,
        PRIMARY KEY("id")
    )
"""


def create_db() -> None:
    connection = sqlite3.connect("cosmetics_shop.db")
    cursor = connection.cursor()
    try:
        cursor.execute(CREATE_USER_TABLE)
        connection.commit()
    except Exception as e:
        print(e)

    connection.close()


if __name__ == "__main__":
    create_db()
