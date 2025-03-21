import dagster as dg
from resources import *
from database import create_tables

DATABASE_URL = dg.EnvVar("DATABASE_URL")

@dg.asset
def api_data(my_conn: ApiDataPostgress):
    return my_conn.request(f"http://{API_HOST}:{API_PORT}/{API_ENDPOINT}",date=DATE,variables=VARIABLES_TO_FETCH).json()


@dg.asset(
    name = "table_creation",
    description = "Create the table in the database",
)
def create_database_tables():
    create_tables(DATABASE_URL)