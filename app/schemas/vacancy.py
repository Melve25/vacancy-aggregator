from pydantic import BaseModel, HttpUrl
from typing import Optional

class VacancyBase(BaseModel):
	url: HttpUrl
	title: Optional[str] = None
	company: Optional[str] = None
	locations: Optional[str] = None
	description: Optional[str] = None
	status: Optional[str] = 'new'

class VacancyCreate(VacancyBase):
	pass

class VacancyUpdate(BaseModel):
	url: Optional[HttpUrl] = None
	title: Optional[str] = None
	company: Optional[str] = None
	locations: Optional[str] = None
	description: Optional[str] = None
	status: Optional[str] = None

class VacancyRead(VacancyBase):
	id: int
	user_id: int

	class Config:
		from_attributes = True
