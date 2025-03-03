from typing import Any, Dict, Optional

from exceptions import InvalidSalaryError


class Vacancy:
    """Класс, представляющий вакансию.

    Атрибуты:
        name (str): Название вакансии.
        requirements (str): Требования к кандидату.
        salary (Optional[Dict[str, Any]]): Зарплата в виде словаря с ключами 'from' и 'to'.
        url (str): Ссылка на вакансию.
    """

    __slots__ = ("name", "requirements", "salary", "url")

    def __init__(self, name: str, requirements: str, salary: Optional[Dict[str, Any]], url: str) -> None:
        """Инициализация экземпляра класса Vacancy.

        Аргументы:
            name (str): Название вакансии.
            requirements (str): Требования к кандидату.
            salary (Optional[Dict[str, Any]]): Зарплата в виде словаря с ключами 'from' и 'to'.
            url (str): Ссылка на вакансию.
        """
        self.name = name
        self.requirements = requirements
        self.url = url
        self.salary = self.__validate_salary(salary)

    def __validate_salary(self, salary: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Проверяет корректность указания зарплаты.

        Аргументы:
            salary (Optional[Dict[str, Any]]): Зарплата в виде словаря с ключами 'from' и 'to'.

        Возвращает:
            Optional[Dict[str, Any]]: Проверенный словарь зарплаты.

        Исключения:
            InvalidSalaryError: Если зарплата указана в некорректном формате или выходит за допустимые пределы.
        """
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
        """Сравнивает текущую вакансию с другой по зарплате.

        Аргументы:
            other (Vacancy): Вакансия для сравнения.

        Возвращает:
            bool: True, если зарплата текущей вакансии меньше, чем у другой.
        """
        if self.salary is None:
            return False
        if other.salary is None:
            return True
        return (self.salary.get("from") or 0) < (other.salary.get("from") or 0)

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии.

        Возвращает:
            str: Строка с информацией о вакансии.
        """
        return (
            f"Вакансия: {self.name}, Требования: {self.requirements},"
            f" Зарплата: {self.salary if self.salary is not None else 'Не указана'}, Ссылка: {self.url}"
        )
