CREATE USER input_user;
ALTER USER input_user WITH PASSWORD 'input_password';
CREATE DATABASE input_db;
ALTER USER postgres PASSWORD 'admin';

\c input_db



CREATE TABLE data (
    id serial primary key,
    timestamp TIMESTAMP NOT NULL,
    wind_speed FLOAT ,
    power FLOAT,
    ambient_temperature FLOAT);

ALTER TABLE data OWNER TO input_user;

SET TIMEZONE TO 'America/Sao_Paulo';
INSERT INTO data(timestamp, wind_speed, power, ambient_temperature)
SELECT 
    generate_series(now(), now() + interval '10 days', '1 minute') AS timestamp,
    ((random() * 2 - 1)) * 5 + 7 , -- Velocidade do vento entre 2 e 12 km/h
    (random() * 2 - 1) * 6 + 8, -- Potência entre 2 e 14 MW
    (random() * 2 - 1) * 3 + 27; -- Temperatura ambiente entre 24 e 30 graus