from pydantic import BaseModel,Field

class Doctor(BaseModel):
    name:str
    discreption:str
    phone_number:int
    addres:str

class DoctorUpdate(BaseModel):
     name:str|None=Field(min_length=1,max_length=100,default=None)
     discreption:str|None=Field(min_length=800,default=None)
     phone_number:int|None=Field(min_length=11,default=None)
     addres:str|None = Field(min_length=1,max_length=800,default=None)