import gspread
import sqlite3


def sync_data():
    service_account = gspread.service_account()
    work_sheet_items = service_account.open("Test Cosmetic Shop Table").get_worksheet(0)
    items = work_sheet_items.get_all_records()

    with sqlite3.connect("cosmetics_shop.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT item_id, title, category, price FROM items")
        db_data = {row[0]: row for row in cursor.fetchall()}

        for item in items:
            item_id = item["item_id"]
            db_item = db_data.get(item_id)

            if db_item:
                if (
                        item["title"] != db_item[1]
                        or item["category"][0] != db_item[2]
                        or item["price"] != db_item[3]
                ):
                    cursor.execute(
                        "UPDATE items SET title=?, category=?, price=? WHERE item_id=?",
                        (item["title"], item["category"][0], item["price"], item_id),
                    )
            else:
                cursor.execute(
                    "INSERT INTO items (title, category, item_id, price) VALUES (?, ?, ?, ?)",
                    (item["title"], item["category"][0], item_id, item["price"]),
                )

        connection.commit()


if __name__ == "__main__":
    sync_data()
