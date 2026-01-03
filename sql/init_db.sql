
CREATE DATABASE IF NOT EXISTS milware_db CHARACTER SET utf8mb4 COLLATE utf8mb4_czech_ci;
USE milware_db;


DROP TABLE IF EXISTS MissionAssignments;
DROP TABLE IF EXISTS Missions;
DROP TABLE IF EXISTS Vehicles;
DROP TABLE IF EXISTS Soldiers;
DROP TABLE IF EXISTS Bases;


CREATE TABLE Bases (
    base_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(255) NOT NULL,
    established_date DATE,
    capacity INT DEFAULT 100
);

CREATE TABLE Soldiers (
    soldier_id INT AUTO_INCREMENT PRIMARY KEY,
    callsign VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    rank ENUM('Private', 'Corporal', 'Sergeant', 'Lieutenant', 'General') DEFAULT 'Private',
    base_id INT,
    FOREIGN KEY (base_id) REFERENCES Bases(base_id) ON DELETE SET NULL
);

CREATE TABLE Vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    fuel_consumption FLOAT NOT NULL,
    is_combat_ready BOOLEAN DEFAULT TRUE,
    base_id INT,
    FOREIGN KEY (base_id) REFERENCES Bases(base_id) ON DELETE CASCADE
);

CREATE TABLE Missions (
    mission_id INT AUTO_INCREMENT PRIMARY KEY,
    operation_name VARCHAR(100) NOT NULL,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

CREATE TABLE MissionAssignments (
    mission_id INT,
    soldier_id INT,
    role_description VARCHAR(100),
    PRIMARY KEY (mission_id, soldier_id),
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id) ON DELETE CASCADE,
    FOREIGN KEY (soldier_id) REFERENCES Soldiers(soldier_id) ON DELETE CASCADE
);
