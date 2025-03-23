import dagster as dg
import os
from .resources import *
from datetime import datetime, timedelta



DATE = os.getenv("DATE")
VARIABLES_TO_FETCH = os.getenv("VARIABLES_TO_FETCH")

def convert_variable(data: pd.DataFrame, variable: str, timestamp: list) -> pd.DataFrame:
    _data = data[variable]
    _data["timestamp"] = timestamp
    _data["name"] = variable
    return _data

@dg.asset
def api_data(my_conn: ApiDataPostgress):
    return my_conn.request(date=DATE, variables=VARIABLES_TO_FETCH).json()


@dg.asset()
def transform_data(context, api_data, my_db: DatabasePostgress):
    # Transformando os dados JSON em um DataFrame e agrupando os dados 10-minutal
    client = my_db.get_client()
    if client.date_exists(DATE, "signal"):
        context.log.info("Data already exists")
        return None, None
    df = pd.DataFrame(api_data)
    _data = df.groupby(np.arange(len(df))//10)

    _data = _data.agg({"wind_speed": ["mean", "std", "min", "max"], "power": ["mean", "std", "min", "max"]})
    # Criando o timestamp 10-minutal para inserir no banco de dados
    timestamp =  [ datetime.strptime(DATE, "%d/%m/%Y") + timedelta(minutes=10*i) for i in range(len(_data))]

    wind_speed_data = convert_variable(_data, "wind_speed", timestamp)
    power_data = convert_variable(_data, "power", timestamp)

    return wind_speed_data, power_data


@dg.asset()
def insert_data(context,transform_data, my_db: DatabasePostgress):
    client = my_db.get_client()
    if None in transform_data:
        context.log.info("Data already exists")
        return  
    wind_speed_data, power_data = transform_data

    client.insert_data(wind_speed_data, "signal")
    client.insert_data(power_data, "signal")
    context.log.info("Data inserted successfully")
