# from typing import Any, Dict, List
#
# import requests
#
# from src.api.base_api import BaseAPI
# from exceptions import VacancyNotFoundError
#
#
# class HeadHunterAPI(BaseAPI):
#     BASE_URL = "https://api.hh.ru/vacancies"
#
#     def __init__(self) -> None:
#         """Инициализация экземпляра класса BaseAPI."""
#         self._vacancies: List[Dict[str, Any]] = []
#
#     def _fetch_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
#         """Приватный метод для отправки запросов к API hh.ru."""
#         response = requests.get(self.BASE_URL, params=params)
#         response.raise_for_status()
#
#
#         data = response.json()
#         if not isinstance(data, dict):
#             raise ValueError("Expected a dictionary from the response JSON.")
#
#         return data
#
#     def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
#         """Получает вакансии по заданному запросу."""
#         params: Dict[str, Any] = {"text": query, "per_page": 20, "page": 0}
#
#         while params["page"] < 20:
#             data = self._fetch_data(params)
#
#             if "items" not in data:
#                 raise VacancyNotFoundError("No vacancies found.")
#
#             self._vacancies.extend(data["items"])
#
#             params["page"] += 1
#
#         return self._vacancies
