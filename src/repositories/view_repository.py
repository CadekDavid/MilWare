from database import Database


class ViewRepository:
    def __init__(self):
        self.db = Database.get_instance()

    def get_soldier_details(self):
        query = "SELECT soldier_id, callsign, rank_, base_name, location FROM View_Soldier_Details"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_mission_status(self):
        query = "SELECT operation_name, start_time, assigned_soldiers FROM View_Mission_Status"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows