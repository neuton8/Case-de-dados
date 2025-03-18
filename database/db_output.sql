CREATE USER output_user;
ALTER USER output_user WITH PASSWORD 'output_password';
CREATE DATABASE output_db;

ALTER DATABASE output_db OWNER TO output_user;
