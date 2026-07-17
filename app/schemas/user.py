from pydantic import EmailStr , Field , BaseModel , ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username : str = Field(
        min_length=3,
        max_length=100
    )
    email : EmailStr
    password : str = Field(
        min_length=8,
        max_length=128
    )
    
class UserResponse(BaseModel):
    id : int
    username : str
    is_active : bool
    email : EmailStr
    created_at : datetime
    model_config = ConfigDict(
        from_attributes=True
    )