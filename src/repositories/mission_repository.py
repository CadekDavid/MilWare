from database import Database
from models.mission import Mission


class MissionRepository:
    def __init__(self):
        self.db = Database.get_instance()

    def get_all(self):
        query = "SELECT mission_id, operation_name, start_time, description FROM Missions"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        missions = []
        for row in rows:
            missions.append(Mission(row[0], row[1], row[2], row[3]))

        cursor.close()
        return missions

    def assign_soldier(self, mission_id, soldier_id, role):
        query_ass = "INSERT INTO MissionAssignments (mission_id, soldier_id, role_description) VALUES (%s, %s, %s)"
        query_update_soldier = "UPDATE Soldiers SET callsign = CONCAT(callsign, '*') WHERE soldier_id = %s"
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            print(f"--- ZAHAJUJI TRANSAKCI (Mise + Voják) ---")
            cursor.execute(query_ass, (mission_id, soldier_id, role))
            cursor.execute(query_update_soldier, (soldier_id,))
            conn.commit()
            print("--- COMMIT (Obě tabulky uloženy) ---")
            return True

        except Exception as e:
            print(f"Chyba přiřazení: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def get_mission_crew(self, mission_id):
        query = """
            SELECT s.full_name, s.rank_, ma.role_description
            FROM Soldiers s
            JOIN MissionAssignments ma ON s.soldier_id = ma.soldier_id
            WHERE ma.mission_id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (mission_id,))
        crew = cursor.fetchall()
        cursor.close()
        return crew



    def get_all_assignments(self):
        query = """
            SELECT m.operation_name, s.full_name, ma.role_description
            FROM MissionAssignments ma
            JOIN Missions m ON ma.mission_id = m.mission_id
            JOIN Soldiers s ON ma.soldier_id = s.soldier_id
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows