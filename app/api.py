from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import schemas
from . import crud
from .database import get_db

router = APIRouter()

@router.get("/create_task")
def create_task(
        name: str,
        description: str,
        status: str = 'created',
        db: Session = Depends(get_db)
):
    task = schemas.Task(
        name = name,
        description = description,
        status = status
    )
    res = crud.create_task(db, task)

    if not res:
        raise HTTPException(status_code=404, detail="the status is invalid")

    return res

@router.get("/get_task")
def get_task(
        id:str,
        db: Session = Depends(get_db)
):
    filters = schemas.TaskFilter(
        id = id
    )
    res = crud.get_task(db, filters)
    if not res:
        raise HTTPException(status_code=404, detail="the id is invalid")
    return res

@router.get("/get_list_task")
def get_list_task(
    db: Session = Depends(get_db)
):
    res = crud.get_list_task(db)
    return res

@router.get("/update_task")
def update_task(
    id: str,
    name: str | None = None,
    description: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    update_task = schemas.TaskUpdate(
        id = id,
        name = name,
        description = description,
        status = status
    )
    res = crud.update_task(db, update_task)
    if not res:
        raise HTTPException(status_code=404, detail="the parameters are not valid")
    return res

@router.get("/delete_task")
def delete_task(
        id:str,
        db: Session = Depends(get_db)
):
    filters = schemas.TaskFilter(
        id = id
    )
    res = crud.delete_task(db, filters)
    if not res:
        raise HTTPException(status_code=404, detail="the id is invalid")
    return res
