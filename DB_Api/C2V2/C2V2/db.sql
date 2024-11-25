-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS C2;
USE C2;

-- Step 2: General Entities Table
CREATE TABLE entities (
    entity_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('Plane', 'Ship', 'LandForce', 'User') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Plane Table with JSON Fields
CREATE TABLE plane (
    plane_id INT AUTO_INCREMENT PRIMARY KEY,
    entry_id INT,
    entity_id INT NOT NULL,
    latitude FLOAT,  -- For "Latitude"
    longitude FLOAT, -- For "Longitude"
    enemy INT,   -- To store "Enemy"
    time_position DATETIME, -- To store "Time_position"
    geo_altitude FLOAT, -- To store "Geo_altitude"
    velocity FLOAT, -- To store "Velocity"
    true_track FLOAT, -- To store "True_track"
    call_sign VARCHAR(255), -- To store "Call_sign"
    origin_country VARCHAR(255), -- To store "Origin_country"
    on_ground INT, -- To store "On_ground"
    category INT, -- To store "Category"
    size VARCHAR(50), -- To store "Size"
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

-- Step 4: Example Tables for Ship, LandForce, User
CREATE TABLE ship (
    ship_id INT AUTO_INCREMENT PRIMARY KEY,
    entry_id INT,
    entity_id INT NOT NULL,
    ship_name VARCHAR(255),
    ship_type VARCHAR(255),
    displacement INT,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE TABLE landforce (
    landforce_id INT AUTO_INCREMENT PRIMARY KEY,
    entry_id INT,
    entity_id INT NOT NULL,
    unit_name VARCHAR(255),
    unit_size INT,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id INT NOT NULL,
    username VARCHAR(255),
    role VARCHAR(255),
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

