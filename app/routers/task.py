# app/routers/task.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.task import TaskCreate, TaskDB, TaskResponse
from app.db import get_db, TaskModel

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=task.completed,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Convert TaskModel to a dictionary using __dict__
    db_task_dict = db_task.__dict__
    
    # Exclude internal SQLAlchemy attributes
    db_task_dict.pop("_sa_instance_state", None)
    
    # Return the response model using the dictionary
    return TaskResponse(**db_task_dict)



@router.get("/tasks/", response_model=list[TaskDB])
async def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskDB)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskDB)
async def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete the task
    db.delete(db_task)
    db.commit()

    # Return a simple dictionary as the response
    return {"message": f"Task {task_id} deleted", "deleted_task_id": task_id}