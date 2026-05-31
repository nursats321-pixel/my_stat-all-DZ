from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from database import Base, engine
from models import Task
from database import get_db
from schemas import TaskCreate
from services import create_task, get_all_tasks


app = FastAPI()


@app.get("/tasks/")
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await get_all_tasks(db)




@app.post("/tasks/")
async def tasks_valid(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        tasks = await create_task(db, task_data)
        return tasks
    
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)