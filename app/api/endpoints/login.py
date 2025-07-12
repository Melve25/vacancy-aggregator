from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt


from app.schemas.token import Token, TokenData
from app.schemas.user import UserRead
from app.crud.user import get_user_by_email
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/jwt/login')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)) -> User:
	"""
	Декорирует токен и возвращает пользователя.
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={'WWW-Authenticate': 'Bearer'}
	)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		email: str = payload.get('sub')
		if email is None:
			raise credentials_exception
		token_data = TokenData(email=email)
	except JWTError:
		raise credentials_exception
	
	user = await get_user_by_email(db, email=token_data.email)
	if user is None:
		raise credentials_exception
	
	return user


@router.post('/auth/jwt/login', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
	"""
	Аутентификация пользователя и возврат JWT токен.
	"""
	user = await get_user_by_email(db, email=form_data.username)
	if not user or not security.verify_password(form_data.password, user.hashed_password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect email or password',
			headers={'WWW-Authenticate': 'Bearer'}
		)
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = security.create_access_token(
		data={'sub': user.email}, expirers_delta=access_token_expires
	)
	return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me', response_model=UserRead)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
	"""
	Получение данных о текущем аутентифицированном пользователе.
	"""
	return current_user