from typing import Any, Dict, Optional

from exceptions import InvalidSalaryError


class Vacancy:
    __slots__ = ("name", "requirements", "salary", "url")

    def __init__(self, name: str, requirements: str, salary: Optional[Dict[str, Any]], url: str) -> None:
        """Инициализация экземпляра класса Vacancy."""
        self.name = name
        self.requirements = requirements
        self.url = url
        self.salary = self.__validate_salary(salary)

    def __validate_salary(self, salary: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Проверяет корректность указания зарплаты."""
        if salary is not None:
            if isinstance(salary, dict):

                from_ = salary.get("from", None)
                to = salary.get("to", None)

                if from_ is not None and to is not None and from_ > to:
                    raise InvalidSalaryError("Минимальная зарплата выше максимальной.")

                if from_ is not None and from_ < 0:
                    raise InvalidSalaryError("Зарплата не может быть отрицательной.")
                if to is not None and to < 0:
                    raise InvalidSalaryError("Зарплата не может быть отрицательной.")
            else:
                raise InvalidSalaryError("Неправильный формат зарплаты.")

        return salary

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий по зарплате."""
        if self.salary is None:
            return False
        if other.salary is None:
            return True
        return (self.salary.get("from") or 0) < (other.salary.get("from") or 0)

    def __str__(self) -> str:
        """Строковое представление вакансии."""
        return (
            f"Вакансия: {self.name}, Требования: {self.requirements},"
            f" Зарплата: {self.salary if self.salary is not None else 'Не указана'}, Ссылка: {self.url}"
        )
