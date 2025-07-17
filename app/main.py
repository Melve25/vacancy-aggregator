from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter

from app.api.handlers import api_router
from app.graphql.schema import schema
from app.db.session import get_db
from app.api.endpoints.login import get_current_user_graphql


async def get_context(
	request: Request,
	db: AsyncSession = Depends(get_db),
):
	"""
	Создает контекст, который будет доступен во всех GraphQL-резолверах.
	"""
	try:
		current_user = await get_current_user_graphql(request, db)
	except Exception:
		current_user = None

	return {
		'db': db,
		'current_user': current_user
	}


graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)
app = FastAPI(title="Vacancy Aggregator")

app.include_router(api_router)
app.include_router(graphql_app, prefix='/graphql')

@app.get('/')
async def root():
	"""
	Простой эндпоинт для проверки, что сервис работает.
	"""
	
	return {'message': 'Service is running'}