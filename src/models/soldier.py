class Soldier:
    def __init__(self, soldier_id, callsign, full_name, rank_, base_id):
        self.soldier_id = soldier_id
        self.callsign = callsign
        self.full_name = full_name
        self.rank = rank_
        self.base_id = base_id

    def __str__(self):
        return f"[{self.rank}] {self.full_name} ('{self.callsign}')"