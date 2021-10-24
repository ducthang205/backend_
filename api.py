from fastapi import FastAPI
from sqlalchemy import create_engine
from starlette.middleware.cors import CORSMiddleware

from database import engine

from db.schema import ConditionRecord

app = FastAPI()

# Dependency

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/get_record/{page}/{limit}", tags=["records"])
async def get_record(page: int, limit: int):
    with engine.connect() as con:
        print(con)
        rs = con.execute('SELECT * FROM records ORDER BY id DESC ')
        list = []
        i = 0

        for row in rs:
            print()
            if i < (page - 1) * limit: continue
            if i > page * limit - 1: break
            list.append(row)
            i = i + 1
        rs.close()
    return list


@app.put(
    "/set_condition/{key}/{price}/{vol}", tags=["conditions"]
)
async def set_condition(con: ConditionRecord, key: str, price: int, vol: int):
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = engine.connect()
    _conn.execute("INSERT INTO condition (key, price, vol) VALUES (:key, :price, :vol)", key=key,price=price, vol=vol)
    rs = _conn.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')
    print(rs)


@app.get("/get_condition", tags=["conditions"])
async def get_condition():
    with engine.connect() as con:
        rs = con.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')
        list = []
        for row in rs:
            list.append(row)
        rs.close()
    return list
