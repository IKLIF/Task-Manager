from sqlalchemy.orm import Session
from . import models, schemas
import uuid

def cheak_uuid(id):
    try:
        uuid_obj = uuid.UUID(id)
        return True
    except ValueError:
        return

def create_task(db: Session, user_task: schemas.Task):
    if not user_task.status in ['created', 'in progress', 'completed']:
        return None

    db_user = models.Task(
        id=uuid.uuid4(),
        name = user_task.name,
        description = user_task.description,
        status = user_task.status,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_task(db: Session, filter: schemas.TaskFilter):
    if not cheak_uuid(filter.id):
        return

    query = db.query(models.Task)

    if filter.id is not None:
        query = query.filter(models.Task.id == filter.id)
    return query.first()

def get_list_task(db: Session):
    query = db.query(models.Task)
    return [{'name':task.name, 'id': task.id, 'status':task.status, 'description': f'{task.description[:25]}...' if task.description else None} for task in query.all()]

def update_task(db: Session, task_update: schemas.TaskUpdate):
    if not cheak_uuid(task_update.id):
        return
    db_task = db.query(models.Task).filter(models.Task.id == task_update.id).first()

    if not db_task:
        return None#

    match db_task.status:
        case 'created':
            if not task_update.status in ['created', 'in progress', 'completed', None]:
                return None
        case 'in progress':
            if not task_update.status in ['in progress', 'completed', None]:
                return None
        case 'completed':
            if not task_update.status in ['completed', None]:
                return None



    update_data = task_update.dict(exclude_unset=True)

    # Обновляем только те поля, которые были явно переданы (даже если они None)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_task, field, value)

    # Сохраняем изменения
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, filter: schemas.TaskFilter):
    if not cheak_uuid(filter.id):
        return

    db_task = db.query(models.Task).filter(models.Task.id == filter.id).first()

    if not db_task:
        return

    db.delete(db_task)
    db.commit()

    return db_task