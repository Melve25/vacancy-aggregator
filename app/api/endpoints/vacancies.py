from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.vacancy import VacancyRead, VacancyParseRequest, VacancyUpdate
from app.models.user import User
from app.crud.vacancy import create_user_vacancy, get_vacancies_by_user, get_vacancy
from app.api.endpoints.login import get_current_user
from app.db.session import get_db
from app.services.parser import parse_vacancy_from_url

router = APIRouter()

@router.post('/parse', response_model=VacancyRead)
async def parse_and_create_vacancy(
	request: VacancyParseRequest,
	db: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
	"""
	Парсит данные по URL и сохраняет её в БД.
	"""
	try:
		parse_data = await parse_vacancy_from_url(str(request.url))
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
	
	return await create_user_vacancy(db=db, vacancy=parse_data, user_id=current_user.id)

@router.get('/', response_model=List[VacancyRead])
async def read_vacancies(
	skip: int = 0,
	limit: int = 100,
	db: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
	"""
	Получает список всех вакансий текущего пользователя.
	"""
	vacancies = await get_vacancies_by_user(db=db, user_id=current_user.id)
	return vacancies

@router.put('/{vacancy_id}', response_model=VacancyRead)
async def update_vacancy_status(
	vacancy_id: int,
	vacancy_in: VacancyUpdate,
	db: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
	"""
	Обновляет статус или другие данные вакансии.
	"""
	db_vacancy = await get_vacancy(db=db, vacancy_id=vacancy_id, user_id=current_user.id)
	if not db_vacancy:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
	
	update_data = vacancy_in.model_dump(exclude_unset=True)
	for field, value in update_data.items():
		setattr(db_vacancy, field, value)

	await db.commit()
	await db.refresh(db_vacancy)
	return db_vacancy