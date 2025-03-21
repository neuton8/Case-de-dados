from dagster import Definitions, load_assets_from_modules
from . import assets
from .etl import resources as etl
##### Extraction
extraction_assets = load_assets_from_modules([etl])


defs = Definitions(
    assets=extraction_assets,
    resources={
        "my_conn": etl.ApiDataPostgress(),
    },
)
