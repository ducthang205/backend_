from db import schema, models
from database import conn
from db.models import records, condition


def create_record(record: schema.CreateRecord):
    record = models.Records(
        id=record.id,
        time=record.time,
        price=record.price,
        change=record.change,
        per=record.per,
        vol=record.vol,
        totalVol=record.totalVol,
        density=record.density,

    )
    result = conn.execute(records.insert().values(record))
    return conn.execute(records.select().where(record.c.id == result.lastrowid)).first()


def get_condition():
    rs = conn.execute(condition.select()).first()
    print(rs)
    return rs


get_condition()
