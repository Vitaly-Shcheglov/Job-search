class ZeroQuantityError(Exception):
    """Исключение, вызываемое при попытке установить количество в ноль."""

    def __init__(self, message: str = "Товар с нулевым количеством не может быть добавлен."):
        self.message = message
        super().__init__(self.message)


class InvalidSalaryError(Exception):
    """Исключение, вызываемое при неверном указании зарплаты."""

    def __init__(self, message: str = "Зарплата должна быть положительной."):
        self.message = message
        super().__init__(self.message)


class VacancyNotFoundError(Exception):
    """Исключение, вызываемое, когда вакансия не найдена."""

    def __init__(self, message: str = "Вакансии не найдены."):
        self.message = message
        super().__init__(self.message)
