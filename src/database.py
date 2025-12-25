#import mysql.connector
import json
import os


class Database:
    _instance = None

    def __init__(self):
        if Database._instance is not None:
            raise Exception("Použij metodu get_instance().")

        self._connection = None
        self._config = self._load_config()

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def _load_config(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config.json')

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Konfigurační soubor neexistuje: {config_path}. Vytvoř ho podle config.example.json")

        with open(config_path, 'r') as file:
            return json.load(file)

    def connect(self):
        try:
            if self._connection is None or not self._connection.is_connected():
                print(f"Připojuji se k DB: {self._config['db_name']}...")
                self._connection = mysql.connector.connect(
                    host=self._config['db_host'],
                    user=self._config['db_user'],
                    password=self._config['db_pass'],
                    database=self._config['db_name']
                )
                print("Spojení úspšné.")
        except mysql.connector.Error as err:
            print(f"Chyba při připojování: {err}")
            raise

    def get_connection(self):
        self.connect()
        return self._connection