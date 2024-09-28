import abc
import requests
from src.job_vacancy import JobVacancy


class AbstractJobService(abc.ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abc.abstractmethod
    def connect(self) -> bool:
        """Подключение к API."""
        pass

    @abc.abstractmethod
    def get_vacancies(self, query: str, area: str) -> list:
        """Получение вакансий по запросу."""
        pass


class HHJobService(AbstractJobService):
    """Класс для работы с API hh.ru."""

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self._session = requests.Session()

    def connect(self) -> bool:
        """Подключение к API hh.ru."""
        try:
            response = self._session.get(self.BASE_URL)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")
            return False

    def get_vacancies(self, query: str, area: str) -> list:
        """Получение вакансий по ключевому слову."""
        params = {
            'text': query,
            'area': area,
        }

        response = self._session.get(self.BASE_URL, params=params)
        response.raise_for_status()

        vacancy_data = response.json().get('items', [])
        vacancies = []

        for data in vacancy_data:
            title = data['name']
            url = data['alternate_url']

            salary_info = data.get('salary')
            if salary_info:
                salary = salary_info.get('from', 0)  # Используем только нижнюю границу
            else:
                salary = None

                # Извлекаем данные из snippet
            snippet = data.get('snippet', {})
            responsibilities = snippet.get('responsibility', 'Нет информации об обязанностях.')
            requirements = snippet.get('requirement', 'Нет информации о требованиях.')

            description = responsibilities  # Сохраняем обязанности в описании

            vacancies.append(JobVacancy(
                title=title,
                url=url,
                salary=salary,
                description=description,
                requirements=requirements  # Сохраняем требования
            ))

        return vacancies
