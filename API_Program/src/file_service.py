import abc
import json
from src.job_vacancy import JobVacancy


class AbstractFileService(abc.ABC):
    @abc.abstractmethod
    def load(self) -> list:
        pass

    @abc.abstractmethod
    def save(self, vacancies: list):
        pass

    @abc.abstractmethod
    def delete(self, vacancy_title: str):
        pass


class JsonFileService(AbstractFileService):
    def __init__(self, filename: str = 'vacancies.json'):
        self._filename = filename

    def load(self) -> list:
        try:
            with open(self._filename, 'r') as f:
                data = json.load(f)
                return [JobVacancy(**item) for item in data]
        except FileNotFoundError:
            return []

    def save(self, vacancies: list):
        existing_vacancies = self.load()
        for vacancy in vacancies:
            if vacancy not in existing_vacancies:  # Проверка на дубликаты
                existing_vacancies.append(vacancy)
        with open(self._filename, 'w') as f:
            json.dump([vacancy.__dict__ for vacancy in existing_vacancies], f)

    def delete(self, vacancy_title: str):
        existing_vacancies = self.load()
        updated_vacancies = [vac for vac in existing_vacancies if vac.title != vacancy_title]
        with open(self._filename, 'w') as f:
            json.dump([vacancy.__dict__ for vacancy in updated_vacancies], f)