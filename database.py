from sqlalchemy import create_engine, MetaData

engine = create_engine("sqlite:///./sql_app.db")

meta = MetaData()
conn = engine.connect()


