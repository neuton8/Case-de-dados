import dagster as dg
from .etl import assets, resources



##### Extraction
assets = dg.load_assets_from_modules([assets])



defs = dg.Definitions(
    assets=assets,
    resources={
        "my_conn": resources.ApiDataPostgress(api_host=dg.EnvVar("API_HOST"), api_port=dg.EnvVar("API_PORT"), api_endpoint=dg.EnvVar("API_ENDPOINT")),
        "my_db": resources.DatabasePostgress(url = dg.EnvVar("DATABASE_URL")),
    },
)
