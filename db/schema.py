from pydantic import BaseModel


# TO support creation and update APIs
class CreateRecord(BaseModel):
    id: str
    time: str
    price: str
    change: str
    per: str
    vol: str
    totalVol: str
    density: str


class ConditionRecord(BaseModel):
    id: str
    key: str
    price: str
    vol: str

