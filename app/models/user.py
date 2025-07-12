from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.vacancy import Vacancy


class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
	hashed_password: Mapped[str] = mapped_column(String, nullable=False)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True)

	vacancies: Mapped[list['Vacancy']] = relationship(back_populates='user', cascade='all, delete-orphan')