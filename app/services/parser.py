import httpx
from bs4 import BeautifulSoup

from app.schemas.vacancy import VacancyCreate

async def parse_vacancy_from_url(url: str) -> VacancyCreate:
	"""
	Парсит данные вакансии со страницы hh.ru
	ПРИМЕЧАНИЕ: Селекторы могут измениться. Это просто пример.
	"""
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}
	async with httpx.AsyncClient() as client:
		try:
			response = await client.get(url, headers=headers, follow_redirects=True)
			response.raise_for_status()
		except httpx.RequestError as exc:
			raise ValueError(f'Ошибка при запросе к URL {url}: {exc}')
		
	soup = BeautifulSoup(response.text, 'html.parser')

	title = soup.find('h1', {'data-qa': 'vacancy-title'}).get_text(strip=True) if soup.find('h1', {'data-qa': 'vacancy-title'}) else 'Не найдено'
	company = soup.find('a', {'data-qa': 'vacancy-company-name'}).get_text(strip=True) if soup.find('a', {'data-qa': 'vacancy-company-name'}) else 'Не найдено'
	location = soup.find('p', {'data-qa': 'vacancy-view-location'}) or soup.find('span', {'data-qa': 'vacancy-view-raw-address'})
	location_text = location.get_text(strip=True) if location else 'Не найдено'

	vacancy_data = VacancyCreate(
		url=url,
		title=title,
		company=company,
		location=location_text,
		description="Описание будет добавлено позже"
	)
	return vacancy_data