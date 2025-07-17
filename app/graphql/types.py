import strawberry
from typing import List, Optional

@strawberry.type
class VacancyType:
	"""
	Описание типа вакансии
	"""
	id: int
	url: str
	title: Optional[str]
	company: Optional[str]
	location: Optional[str]
	status: Optional[str]

@strawberry.type
class UserType:
	"""
	Описание типа пользователя
	"""
	id: int
	email: str
	vacancies: List[VacancyType]