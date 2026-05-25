from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base
from database import get_db
from services import get_all_users
from services import create_user
from schemas import UserCreate



app = FastAPI()



@app.get("/users/")
async def read_users(
db: AsyncSession = Depends(get_db)
):
    
    users = await get_all_users(db)
    
    return users


@app.post("/users/")
async def add_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        created_user = await create_user(db, user)

        return created_user

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )