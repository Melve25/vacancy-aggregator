from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
	email: EmailStr

class UserCreate(UserBase):
	password: str

class UserRead(UserBase):
	id: int
	is_active: bool

	class Config: 
		from_attribute = True