import strawberry
from strawberry.types import Info

from app.graphql.types import UserType
from app.crud.vacancy import get_vacancies_by_user

@strawberry.type
class Query:
	"""
	Корневые запросы API
	"""
	@strawberry.field(description='Возвращает данные о текущем аутентифицированном пользователе.')
	async def me(self, info: Info) -> UserType:
		"""
		Возвращает данные о текущем аутентифицированном пользователе.
		"""
		current_user = info.context.get('current_user')
		if not current_user:
			raise Exception("No authenticated")
		
		db = info.context.get('db')
		vacancies = await get_vacancies_by_user(db=db, user_id=current_user.id)

		return UserType(
			id=current_user.id,
			email=current_user.email,
			vacancies=vacancies
		)