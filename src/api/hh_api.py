from typing import Any, Dict, List

import requests

from exceptions import VacancyNotFoundError
from src.api.base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс для взаимодействия с API HeadHunter.

    Этот класс наследует от BaseAPI и реализует методы для получения вакансий из API HeadHunter.
    """

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        """Инициализация экземпляра класса HeadHunterAPI.

        Создает экземпляр класса и инициализирует список вакансий.
        """
        self._vacancies: List[Dict[str, Any]] = []

    def _fetch_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Приватный метод для отправки запросов к API hh.ru.

        Этот метод отправляет GET-запрос к API с указанными параметрами и возвращает данные в формате JSON.

        Аргументы:
            params (Dict[str, Any]): Параметры запроса, которые будут отправлены к API.

        Возвращает:
            Dict[str, Any]: Ответ API в формате JSON, представленный как словарь.

        Исключения:
            requests.HTTPError: Если HTTP-запрос завершился ошибкой.
            ValueError: Если ответ не является словарем.
        """
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Expected a dictionary from the response JSON.")

        return data

    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """Получает вакансии по заданному запросу.

        Этот метод отправляет запрос к API для получения вакансий, соответствующих заданному текстовому запросу.

        Аргументы:
            query (str): Строка поиска для фильтрации вакансий.

        Возвращает:
            List[Dict[str, Any]]: Список вакансий в формате словарей.

        Исключения:
            VacancyNotFoundError: Если вакансии не найдены по заданному запросу.
        """
        params: Dict[str, Any] = {"text": query, "per_page": 20, "page": 0}

        while params["page"] < 20:
            data = self._fetch_data(params)

            if "items" not in data:
                raise VacancyNotFoundError("No vacancies found.")

            self._vacancies.extend(data["items"])
            params["page"] += 1

        return self._vacancies  # Возвращает список вакансий.
