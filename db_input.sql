CREATE USER input_user;
CREATE DATABASE input_db;
GRANT ALL PRIVILEGES ON DATABASE "input_db" TO input_user;

\c input_db

CREATE TABLE data (
    id INT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    wind_speed FLOAT ,
    power FLOAT,
    ambient_temperature FLOAT);

