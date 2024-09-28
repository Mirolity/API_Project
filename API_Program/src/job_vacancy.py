class JobVacancy:
    """Класс, представляющий вакансию."""

    __slots__ = ('title', 'url', 'salary', 'description', 'requirements')

    def __init__(self, title: str, url: str, salary: float = None,
                 description: str = "", requirements: str = ""):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description
        self.requirements = requirements

    def _validate_salary(self, salary: float) -> float:
        """Валидация значения зарплаты."""
        if salary is None:
            return "Зарплата не указана"
        elif isinstance(salary, (int, float)) and salary >= 0:
            return salary
        else:
            raise ValueError("Некорректное значение зарплаты. Должно быть неотрицательное число.")

    def __lt__(self, other: 'JobVacancy') -> bool:
        """Метод для сравнения вакансий по зарплате."""
        return self.salary < other.salary

    def __repr__(self) -> str:
        """Строковое представление вакансии."""
        return (f"JobVacancy(title='{self.title}', url='{self.url}', "
                f"salary={self.salary}, description='{self.description}', "
                f"requirements='{self.requirements}')")