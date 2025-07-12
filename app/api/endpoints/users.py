from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserRead, UserCreate
from app.db.session import get_db

router = APIRouter()

@router.post('/register', response_model=UserRead)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
	"""
	Регистрация нового пользователя.
	"""
	db_user = await get_user_by_email(db, email=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail='Email already registered')
	return await create_user(db=db, user=user)