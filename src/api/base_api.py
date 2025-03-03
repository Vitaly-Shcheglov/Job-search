from abc import ABC, abstractmethod
from typing import Dict, List


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает вакансии по заданному запросу."""
        pass
