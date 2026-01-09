from database import Database

class VehicleRepository:
    def __init__(self):
        self.db = Database.get_instance()

    def get_all(self):
        query = "SELECT vehicle_id, model, fuel_consumption, is_combat_ready, base_id FROM Vehicles"
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def import_from_json(self, data_list):
        query = "INSERT INTO Vehicles (model, fuel_consumption, is_combat_ready, base_id) VALUES (%s, %s, %s, %s)"
        conn = self.db.get_connection()
        cursor = conn.cursor()
        count = 0
        try:
            for item in data_list:
                val = (item['model'], item['fuel'], item['ready'], item['base_id'])
                cursor.execute(query, val)
                count += 1
            conn.commit()
            return count
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()