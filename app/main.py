from fastapi import FastAPI ,Body,status,HTTPException,Path
from typing import Annotated
from app.core.database import create_db_and_tables
from app.schima.doctor import Doctor,DoctorUpdate
from app.models.doctor import Doctor as DoctorDB
from app.dependenciec import SessionDep
from sqlmodel import select


app = FastAPI()
create_db_and_tables()


@app.post('/creat')
async def creat_doctor(
    doctor_info:Annotated[Doctor ,Body()],
    session:SessionDep
):
    doctor_for_db=DoctorDB(
        name=doctor_info.name,
        discreption=doctor_info.discreption,
        phone_number=doctor_info.phone_number,
        addres=doctor_info.addres 
    )
    session.add(doctor_for_db)
    session.commit()
    return doctor_for_db

@app.get(
    '/doctors',
    status_code=status.HTTP_200_OK
)
async def show_doctors(
    session:SessionDep
):
    return session.exec(select(DoctorDB)).all


@app.get('/doctors/{id:int} ', response_model=DoctorDB)
async def get_doctor_by_id(
    id:Annotated[int ,Path()],
    session:SessionDep
) ->DoctorDB:
    doctor_for_db = session.exec(select(DoctorDB).where(DoctorDB.id==id)).first()


    if not doctor_for_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="doctor not found")


    return doctor_for_db
@app.delete('/doctors/{id:int}',status_code=status.HTTP_204_NO_CONTENT)
async def delate_doctor_by_id(
    id:Annotated[int,Path()],
    session:SessionDep
) ->None:
    doctor_from_db=session.exec(select(DoctorDB).where(DoctorDB.id==id)).first()
    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="doctor not found")
    
    
    
    
    session.delete(doctor_from_db)
    session.commit()



@app.patch('/doctors/{id:int}/update')
async def update(
    id:Annotated[int,Path()],
    new_info:Annotated[DoctorUpdate,Body()],
    session:SessionDep
):
    doctor_from_db=session.exec(select(DoctorDB).where(DoctorDB.id==id)).first()
    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="doctor not found")
    session.commit()
    session.refresh(doctor_from_db)