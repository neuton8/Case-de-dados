CREATE USER output_user;
ALTER USER output_user WITH PASSWORD 'output_user';
GRANT pg_read_all_data TO output_user;
GRANT pg_write_all_data TO output_user;
ALTER USER postgres PASSWORD 'admin';
