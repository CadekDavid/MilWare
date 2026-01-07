class Soldier:
    def __init__(self, soldier_id, callsign, full_name, rank, base_id):
        self.soldier_id = soldier_id
        self.callsign = callsign
        self.full_name = full_name
        self.rank = rank
        self.base_id = base_id

    def __str__(self):
        return f"[{self.rank}] {self.full_name} ('{self.callsign}')"