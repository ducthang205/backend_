from sqlalchemy import Column, Integer, String, Table
from database import meta, engine

records = Table(
    "records",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=1),
    Column("time", String(255), ),
    Column("price", String(255)),
    Column("change", String(255)),
    Column("per", String(255), ),
    Column("vol", String(255)),
    Column("totalVol", String(255)),
    Column("density", String(255)),

)
condition = Table(
    "condition",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=1),
    Column("price", String(255), ),
    Column("vol", String(255)),

)

meta.create_all(engine)
