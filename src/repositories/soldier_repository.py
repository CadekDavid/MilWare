from database import Database
from models.soldier import Soldier


class SoldierRepository:
    def __init__(self):
        self.db = Database.get_instance()

    def get_all(self):

        query = "SELECT soldier_id, callsign, full_name, rank, base_id FROM Soldiers"

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
        query = "SELECT soldier_id, callsign, full_name, rank, base_id FROM Soldiers WHERE soldier_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (soldier_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Soldier(row[0], row[1], row[2], row[3], row[4])
        return None

    def create(self, soldier):
        query = "INSERT INTO Soldiers (callsign, full_name, rank, base_id) VALUES (%s, %s, %s, %s)"
        val = (soldier.callsign, soldier.full_name, soldier.rank, soldier.base_id)

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, val)
        conn.commit()

        new_id = cursor.lastrowid
        soldier.soldier_id = new_id
        cursor.close()
        return new_id