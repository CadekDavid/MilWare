from database import Database
import sys


def main():
    print("Start aplikace...")

    try:
        db = Database.get_instance()
        conn = db.get_connection()

        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Jsi připojen k databázi: {record[0]}")

        cursor.close()
    except Exception as e:
        print(f"Kritická chyba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()