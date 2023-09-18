import os.path
import sqlite3

from dotenv import load_dotenv


class Manager:
    def __init__(self):
        load_dotenv()
        self.database_path = os.getenv("DB_PATH")
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
