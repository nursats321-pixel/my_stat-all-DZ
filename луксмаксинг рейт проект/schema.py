from pydantic import BaseModel


class Face(BaseModel):
    name: str
    jawline: int
    height: int
    hair: int
    skin: int
    
    status: str | None = None