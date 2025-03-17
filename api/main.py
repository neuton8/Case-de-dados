from fastapi import FastAPI,Depends,HTTPException
from datetime import datetime,timedelta
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os

#engine = create_engine("postgresql+psycopg2://input_user:input_password@localhost:5433/input_db")
engine = create_engine(os.environ.get("DATABASE_URL"))

def get_session():
    with Session(engine) as session:
        yield session
    
app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]

class Data(SQLModel, table=True):
    id: int  = Field(default=None, primary_key=True)
    timestamp: datetime
    wind_speed: float= None
    power: float = None
    ambient_temperature: float = None

def generate_variables_list(variables):
    if variables:
        variables_list = variables.split(",")
        for variable in variables_list:
            if variable not in Data.__annotations__.keys():
                raise HTTPException(status_code=404, detail="Verifique nome das variaveis")
    else:
        variables_list = list(Data.__annotations__.keys())
    return variables_list

@app.get("/data/")
async def get_table_itens(day: str,session: SessionDep,variables: Optional[str] = None):

    date = datetime.strptime(day, '%d/%m/%Y')
    next_day = date + timedelta(days=1)

    variables_list = generate_variables_list(variables)

    columns = [getattr(Data, variable) for variable in variables_list]
    statement = select(*columns).where(Data.timestamp >= date).where(Data.timestamp < next_day)
    result = session.exec(statement).all()

    try:
        result_dicts = [dict(zip(variables_list, row)) for row in result]
    except ValueError:
        result_dicts = [dict(zip(variables_list, [row])) for row in result] 
    
    return result_dicts

# http://127.0.0.1:8000/data/?data_inicial=14/03/2025&horario_inicial=19:30:00&data_final=15/03/2025&horario_final=19:20:00