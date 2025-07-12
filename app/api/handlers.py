from fastapi import APIRouter

from app.api.endpoints import login, users, vacancies

api_router = APIRouter()
api_router.include_router(login.router, tags=['login'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(vacancies.router, prefix='/vacancies', tags=['vacancies'])