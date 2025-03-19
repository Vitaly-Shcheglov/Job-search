import unittest
from unittest.mock import Mock, patch

import requests  # Добавляем импорт для requests

from exceptions import VacancyNotFoundError
from src.api.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    """Тестовый класс для проверки функциональности класса HeadHunterAPI."""

    def setUp(self) -> None:
        """Инициализация экземпляра HeadHunterAPI перед каждым тестом."""
        self.api = HeadHunterAPI()

    @patch("src.api.hh_api.requests.get")
    def test_get_vacancies_success(self, mock_get: Mock) -> None:
        """Тест успешного получения вакансий.

        Проверяет, что метод get_vacancies возвращает список вакансий
        при успешном выполнении запроса к API.
        """
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "1",
                    "name": "Developer",
                    "salary": {"from": 1000, "to": 2000},
                    "url": "https://api.hh.ru/vacancies",
                },
                {
                    "id": "2",
                    "name": "Tester",
                    "salary": {"from": 800, "to": 1500},
                    "url": "https://api.hh.ru/vacancies",
                },
            ],
            "pages": 1,
        }
        mock_response.raise_for_status = Mock()  # Псевдокод для проверки успешного статуса
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("developer")

        self.assertEqual(vacancies[0]["name"], "Developer")  # Проверка имени первой вакансии
        self.assertEqual(vacancies[1]["name"], "Tester")  # Проверка имени второй вакансии

    @patch("src.api.hh_api.requests.get")
    def test_no_vacancies_found(self, mock_get: Mock) -> None:
        """Тест обработки случая, когда вакансии не найдены.

        Проверяет, что при отсутствии вакансий метод get_vacancies
        вызывает исключение VacancyNotFoundError.
        """
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with self.assertRaises(VacancyNotFoundError):
            self.api.get_vacancies("nonexistent_query")  # Ожидаем, что будет выброшено исключение

    @patch("src.api.hh_api.requests.get")
    def test_http_error(self, mock_get: Mock) -> None:
        """Тест обработки HTTP ошибки.

        Проверяет, что метод get_vacancies вызывает исключение HTTPError
        при возникновении ошибки HTTP.
        """
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")  # Теперь requests доступен
        mock_get.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            self.api.get_vacancies("developer")  # Ожидаем, что будет выброшено исключение HTTPError

    @patch("src.api.hh_api.requests.get")
    def test_response_is_not_dict(self, mock_get: Mock) -> None:
        """Тест обработки случая, когда ответ не является словарем.

        Проверяет, что метод get_vacancies вызывает исключение ValueError
        если ответ от API не является словарем.
        """
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            self.api.get_vacancies("developer")  # Ожидаем, что будет выброшено исключение ValueError


# Запуск тестов
if __name__ == "__main__":
    unittest.main()
