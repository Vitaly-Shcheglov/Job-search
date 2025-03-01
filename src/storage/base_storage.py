from abc import ABC, abstractmethod
from typing import List

from src.models.vacancy import Vacancy


class BaseStorage(ABC):
    """Абстрактный базовый класс для работы с хранилищами данных."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        """Получает все вакансии из хранилища."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из хранилища."""
        pass
