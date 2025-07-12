from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.vacancy import Vacancy
from app.schemas.vacancy import VacancyCreate

async def create_user_vacancy(db: AsyncSession, vacancy: VacancyCreate, user_id: int) -> Vacancy:
    """Создает вакансию для пользователя."""
    data = vacancy.model_dump()
    data['url'] = str(data['url'])

    db_vacancy = Vacancy(**data, user_id=user_id)
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy
    

async def get_vacancies_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    """Получает список вакансий для пользователя."""
    result = await db.execute(
        select(Vacancy).where(Vacancy.user_id == user_id).offset(skip).limit(limit)
    )
    return result.scalars().all()
    
async def get_vacancy(db: AsyncSession, vacancy_id: int, user_id: int) -> Vacancy | None:
    """Получает одну вакансию по ID, проверяя, что она принадлежит пользователю."""
    result = await db.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.user_id == user_id)
	)
    return result.scalars().first()