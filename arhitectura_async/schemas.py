from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    
    name: str
    
    age: int

    email: EmailStr