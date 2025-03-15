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


@app.get("/data/", response_model=list[Data])
async def get_table_itens(data_inicial: str,horario_inicial: str,data_final: str,horario_final: str,session: SessionDep):

    initial_date = datetime.strptime(data_inicial, "%d/%m/%Y")
    initial_time = datetime.strptime(horario_inicial, "%H:%M:%S")
    date_init = initial_date + timedelta(hours=initial_time.hour,minutes=initial_time.minute,seconds=initial_time.second)

    final_date = datetime.strptime(data_final, "%d/%m/%Y")
    final_time = datetime.strptime(horario_final, "%H:%M:%S")
    date_fin = final_date + timedelta(hours=final_time.hour,minutes=final_time.minute,seconds=final_time.second)

    
    statement = select(Data).where(Data.timestamp >= date_init).where(Data.timestamp <= date_fin)
    result = session.exec(statement).all()
    if not result:
        raise HTTPException(status_code=404, detail="Sem dados para esse periodo")

    return JSONResponse(content=jsonable_encoder(result))

# http://127.0.0.1:8000/data/?data_inicial=14/03/2025&horario_inicial=19:30:00&data_final=15/03/2025&horario_final=19:20:00