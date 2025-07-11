from fastapi import FastAPI

app = FastAPI(title="Vacancy Aggregator")

@app.get('/')
async def root():
	"""
	Простой эндпоинт для проверки, что сервис работает.
	"""
	
	return {'message': 'Service is running'}