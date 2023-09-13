from managers.manager import Manager


class ItemCategory(Manager):
    def get_titles(self):
        categories_titles = self.cursor.execute(
            "SELECT * FROM 'item category' "
        ).fetchall()
        return [title[-1] for title in categories_titles]  # Will return list of titles
