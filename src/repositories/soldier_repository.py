from database import Database
from models.soldier import Soldier
import json


class SoldierRepository:
    def __init__(self):
        self.db = Database.get_instance()

    def get_all(self):
        query = "SELECT soldier_id, callsign, full_name, rank_, base_id FROM Soldiers"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        soldiers = []
        for row in rows:
            soldier = Soldier(
                soldier_id=row[0],
                callsign=row[1],
                full_name=row[2],
                rank=row[3],
                base_id=row[4]
            )
            soldiers.append(soldier)

        cursor.close()
        return soldiers

    def get_by_id(self, soldier_id):
        query = "SELECT soldier_id, callsign, full_name, rank_, base_id FROM Soldiers WHERE soldier_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (soldier_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Soldier(row[0], row[1], row[2], row[3], row[4])
        return None

    def create(self, soldier):
        query = "INSERT INTO Soldiers (callsign, full_name, rank_, base_id) VALUES (%s, %s, %s, %s)"
        val = (soldier.callsign, soldier.full_name, soldier.rank, soldier.base_id)

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, val)
        conn.commit()

        new_id = cursor.lastrowid
        soldier.soldier_id = new_id
        cursor.close()
        return new_id

    def update(self, soldier):
        if not soldier.soldier_id:
            raise Exception("Nemůžu aktualizovat vojáka bez ID!")

        query = """
            UPDATE Soldiers 
            SET callsign = %s, full_name = %s, rank_ = %s, base_id = %s 
            WHERE soldier_id = %s
        """
        val = (soldier.callsign, soldier.full_name, soldier.rank, soldier.base_id, soldier.soldier_id)

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, val)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(self, soldier_id):

        query = "DELETE FROM Soldiers WHERE soldier_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, (soldier_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def bulk_import_json(self, json_data):
        query = "INSERT INTO Soldiers (callsign, full_name, rank_, base_id) VALUES (%s, %s, %s, %s)"

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            print("--- Zahajuji transakci ---")
            count = 0
            for item in json_data:
                val = (item['callsign'], item['full_name'], item['rank'], item['base_id'])
                cursor.execute(query, val)
                count += 1

            conn.commit()
            print("--- Transakce potvrzena (COMMIT) ---")
            return count

        except Exception as e:
            conn.rollback()
            print(f"!!! CHYBA IMPORTU - VRACÍM ZMĚNY (ROLLBACK) !!!")
            raise e
        finally:
            cursor.close()
