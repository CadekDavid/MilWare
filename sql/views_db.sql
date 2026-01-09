USE milware_db;

CREATE OR REPLACE VIEW View_Soldier_Details AS
SELECT
    s.soldier_id,
    s.callsign,
    s.full_name,
    s.rank_,
    b.name AS base_name,
    b.location
FROM Soldiers s
JOIN Bases b ON s.base_id = b.base_id;


CREATE OR REPLACE VIEW View_Mission_Status AS
SELECT
    m.operation_name,
    m.start_time,
    COUNT(ma.soldier_id) as assigned_soldiers
FROM Missions m
LEFT JOIN MissionAssignments ma ON m.mission_id = ma.mission_id
GROUP BY m.mission_id, m.operation_name, m.start_time;