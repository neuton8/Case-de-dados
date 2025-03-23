import dagster as dg
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import httpx
from httpx import Response
import os
from .database import create_tables


class ApiDataPostgress(dg.ConfigurableResource):
    api_host: str
    api_port: str
    api_endpoint: str

    def request(self,date: str,variables: str) -> Response:
        url = f"http://{self.api_host}:{self.api_port}/{self.api_endpoint}"
        return httpx.request(
            method="GET",
            url=url,
            params={"day": date, "variables": variables},
            timeout=10,
            follow_redirects=True,)
    
class DatabaseClient:
    def __init__(self, url: str):
        self.url = url
        self.conn = create_engine(self.url)
        create_tables(self.url)

    def insert_data(self, data: pd.DataFrame, table: str):
        data.to_sql(table, self.conn, if_exists="append", index=False)

    def date_exists(self, date: str, table: str) -> bool:
        query = text(f"SELECT EXISTS (SELECT 1 FROM {table} WHERE timestamp = to_date(:date, 'DD/MM/YYYY'))")
        with self.conn.connect() as connection:
            result = connection.execute(query, {"date": date}).scalar()
        return result
    
class DatabasePostgress(dg.ConfigurableResource):
    url: str

    def get_client(self) -> DatabaseClient:
        client = DatabaseClient(self.url)
        return client
