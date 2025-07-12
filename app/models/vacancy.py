from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.user import User

class Vacancy(Base):
	__tablename__ = 'vacancies'

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	url: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
	title: Mapped[str] = mapped_column(String)
	company: Mapped[str] = mapped_column(String, nullable=True)
	location: Mapped[str] = mapped_column(String, nullable=True)
	description: Mapped[str] = mapped_column(Text, nullable=True)
	# new, applied, interview, offer, rejected
	status: Mapped[str] = mapped_column(String, default='new')

	user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
	user: Mapped['User'] = relationship(back_populates='vacancies')
