from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User
from schemas import UserCreate

async def get_all_users(db: AsyncSession):
    
    stmt = select(User)
    
    result = await db.execute(stmt)
    
    return result.scalars().all()


async def create_user(db: AsyncSession, user_data: UserCreate):
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age
    )
    
    if user_data.age < 18:
        
        raise ValueError ("слишком маленький")
        
    
    db.add(new_user)
    
    await db.commit()
    
    await db.refresh(new_user)
    
    return new_user

