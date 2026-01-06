class Mission:
    def __init__(self, mission_id, operation_name, start_time, description):
        self.mission_id = mission_id
        self.operation_name = operation_name
        self.start_time = start_time
        self.description = description

    def __str__(self):
        return f"[{self.mission_id}] Operace: {self.operation_name} ({self.start_time})"