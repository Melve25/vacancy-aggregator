from fastapi import FastAPI

from app.api.handlers import api_router

app = FastAPI(title="Vacancy Aggregator")

app.include_router(api_router)

@app.get('/')
async def root():
	"""
	Простой эндпоинт для проверки, что сервис работает.
	"""
	
	return {'message': 'Service is running'}