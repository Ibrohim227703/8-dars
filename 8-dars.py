import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class ConnectDb:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        self.connection = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host
        )
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def save_to_database(self, connection):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (self.name, self.price))
        connection.commit()

with ConnectDb() as connection:
    products = [Product("Telefon", 999), Product("Kompyuter", 1499)]
    for product in products:
        product.save_to_database(connection)

print()
