from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
	"""
	Получает пользователя по email.
	"""
	result = await db.execute(select(User).where(User.email == email))
	return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
	"""
	Создает нового пользователя.
	"""
	hashed_password = get_password_hash(user.password)
	db_user = User(email=user.email, hashed_password=hashed_password)
	db.add(db_user)
	await db.commit()
	await db.refresh(db_user)
	return db_user