from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""
	Проверяет, совпадение пароля с хэшем
	"""
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
	"""
	Хэширует пароль.
	"""
	return pwd_context.hash(password)


def create_access_token(data: dict, expirers_delta: timedelta | None = None) -> str:
	"""
	Создает JWT-токен.
	"""
	to_encode = data.copy()
	if expirers_delta:
		expire = datetime.now(timezone.utc) + expirers_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)

	to_encode.update({'exp': expire})
	encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
	return encode_jwt