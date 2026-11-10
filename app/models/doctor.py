from sqlmodel import SQLModel ,Field

class Doctor(SQLModel ,table=True):
    id: int |None=Field(primary_key=True,index=True) 
    name:str
    age:int
    discreption:str
    phone_number:int
    addres:str