import unittest
from unittest.mock import patch
from src.job_vacancy import JobVacancy
from src.job_service import HHJobService
from src.file_service import JsonFileService


class TestJobVacancy(unittest.TestCase):

    def test_validate_salary(self):
        vacancy = JobVacancy("Программист", "http://example.com/vacancy/1", salary=100000)
        self.assertEqual(vacancy.salary, 100000)

        vacancy_no_salary = JobVacancy("Программист", "http://example.com/vacancy/1", salary=None)
        self.assertEqual(vacancy_no_salary.salary, "Зарплата не указана")

        with self.assertRaises(ValueError):
            JobVacancy("Программист", "http://example.com/vacancy/1", salary=-1000)

    @patch('requests.Session.get')
    class TestHHJobService(unittest.TestCase):
        def setUp(self):
            self.service = HHJobService()

        def test_connection(self):
            self.assertTrue(self.service.connect(), "Should connect to HH API")

        def test_get_vacancies(self):
            vacancies = self.service.get_vacancies("Программист", "160")
            self.assertIsInstance(vacancies, list, "Should return a list of vacancies")

    class TestJsonFileService(unittest.TestCase):
        def setUp(self):
            self.service = JsonFileService('test_vacancies.json')

        def test_load_empty(self):
            vacancies = self.service.load()
            self.assertEqual(vacancies, [])

        def test_save_load(self):
            vacancy = JobVacancy("Программист", "http://example.com/vacancy/1", salary=100000)
            self.service.save([vacancy])
            loaded_vacancies = self.service.load()
            self.assertEqual(len(loaded_vacancies), 1)

        def test_delete(self):
            vacancy = JobVacancy("Программист", "http://example.com/vacancy/1", salary=100000)
            self.service.save([vacancy])
            self.service.delete("Программист")
            loaded_vacancies = self.service.load()
            self.assertEqual(len(loaded_vacancies), 0)


if __name__ == '__main__':
    unittest.main()