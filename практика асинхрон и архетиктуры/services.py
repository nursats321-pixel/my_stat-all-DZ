from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Task
from schemas import TaskCreate


async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()    

    
async def create_task(db: AsyncSession, task_data: TaskCreate):
    
    if task_data.priority < 1 or task_data.priority > 5:
        raise ValueError("Приоритет должен быть в диапозоне от 1 до 5")


    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        is_completed=False
    )
        

    db.add(new_task)
    
    await db.commit()
    
    await db.refresh(new_task)
    
    return new_task
    
    