import dagster as dg
import httpx
from httpx import Response
import os

API_HOST = dg.EnvVar("API_HOST")
API_PORT = dg.EnvVar("API_PORT")
API_ENDPOINT = dg.EnvVar("API_ENDPOINT")
DATE = dg.EnvVar("DATE")
VARIABLES_TO_FETCH = dg.EnvVar("VARIABLES_TO_FETCH")

class ApiDataPostgress(dg.ConfigurableResource):

    def request(self, endpoint: str, date: str, variables = " ") -> Response:
        return httpx.request(
            method="GET",
            url=endpoint,
            params={"day": date, "variables": variables},
            timeout=10,
            follow_redirects=True,)
    
