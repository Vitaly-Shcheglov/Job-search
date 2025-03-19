from abc import ABC, abstractmethod
from typing import Dict, List


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с API вакансий.

    Этот класс определяет интерфейс для работы с API, предоставляющим информацию о вакансиях.
    Все классы, наследующие от BaseAPI, должны реализовать метод get_vacancies.
    """

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает вакансии по заданному запросу.

        Аргументы:
            query (str): Строка поиска для фильтрации вакансий.

        Возвращает:
            List[Dict[str, Any]]: Список словарей, каждый из которых содержит информацию о вакансии.
            Каждый словарь должен содержать такие ключи, как 'name', 'salary', 'requirements', и 'url'.

        Исключения:
            VacancyNotFoundError: Если вакансии не найдены по заданному запросу.
            HTTPError: Если возникает ошибка при запросе к API.
        """
        pass
