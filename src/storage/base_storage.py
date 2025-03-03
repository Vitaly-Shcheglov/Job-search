from abc import ABC, abstractmethod
from typing import List

from src.models.vacancy import Vacancy


class BaseStorage(ABC):
    """Абстрактный базовый класс для работы с хранилищами данных.

    Этот класс определяет интерфейс для работы с различными хранилищами данных вакансий.
    Все классы, наследующие от BaseStorage, должны реализовать методы для добавления,
    получения и удаления вакансий.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище.

        Аргументы:
            vacancy (Vacancy): Объект вакансии, который нужно добавить в хранилище.
        """
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        """Получает все вакансии из хранилища.

        Возвращает:
            List[Vacancy]: Список объектов вакансий, хранящихся в хранилище.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из хранилища.

        Аргументы:
            vacancy (Vacancy): Объект вакансии, который нужно удалить из хранилища.
        """
        pass
