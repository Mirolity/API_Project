import sys
import locale

# Установка локали
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Установка кодировки вывода
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from src.job_service import HHJobService


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    hh_service = HHJobService()  # Инициализация службы работы с вакансиями

    if not hh_service.connect():  # Подключение к API
        return

    area = "1"  # ID нужного региона hh.ru
    all_vacancies = []  # Список для хранения всех вакансий

    while True:
        print("\nДоступные команды:")
        print("1. Поиск вакансий по запросу")
        print("2. Получить топ .. вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Выход")

        choice = input("Введите номер команды: ")

        if choice == '1':
            query = input("Введите поисковый запрос: ")
            all_vacancies = hh_service.get_vacancies(query, area)
            for vacancy in all_vacancies:
                print(vacancy)
        elif choice == '2':
            query = input("Введите поисковый запрос: ")
            n = int(input("Введите количество вакансий для отображения: "))
            vacancies = hh_service.get_vacancies(query, area)
            top_vacancies = sorted(
                vacancies, key=lambda x: x.salary if isinstance(x.salary, (int, float)) else 0,
                reverse=True)[:n]
            for vacancy in top_vacancies:
                print(vacancy)
        elif choice == '3':
            if not all_vacancies:
                print("Сначала выполните поиск вакансий.")
                continue  # Пропускаем итерацию, если вакансий нет

            keyword = input("Введите ключевое слово для поиска в описании: ")
            filtered_vacancies = [
                vacancy for vacancy in all_vacancies
                if keyword.lower() in vacancy.description.lower()
            ]
            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    print(vacancy)
            else:
                print("Вакансии с данным ключевым словом не найдены.")
        elif choice == '4':
            break  # Завершение программы


if __name__ == "__main__":
    user_interaction()