from database import Database


class BaseRepository:
    def __init__(self):
        self.db = Database.get_instance()

    def get_base_statistics(self):

        query = """
            SELECT 
                b.name, 
                b.location, 
                COUNT(DISTINCT s.soldier_id) as soldier_count,
                COUNT(DISTINCT v.vehicle_id) as vehicle_count
            FROM Bases b
            LEFT JOIN Soldiers s ON b.base_id = s.base_id
            LEFT JOIN Vehicles v ON b.base_id = v.base_id
            GROUP BY b.base_id, b.name, b.location
            ORDER BY soldier_count DESC
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        stats = []
        for row in rows:
            stats.append({
                "name": row[0],
                "location": row[1],
                "soldiers": row[2],
                "vehicles": row[3]
            })
        return stats



    def get_all(self):
        query = "SELECT base_id, name, location, capacity FROM Bases"
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows