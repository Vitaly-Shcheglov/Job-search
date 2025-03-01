import os
import sys
import unittest
from typing import Dict, Optional

from exceptions import InvalidSalaryError
from src.models.vacancy import Vacancy

sys.path.append(os.path.abspath("src"))


class TestVacancy(unittest.TestCase):

    def test_vacancy_initialization(self) -> None:
        """Тест успешной инициализации вакансии."""
        salary: Dict[str, Optional[int]] = {"from": 1000, "to": 2000}
        vacancy = Vacancy(name="Developer", requirements="Python, Django", salary=salary, url="http://example.com")

        self.assertEqual(vacancy.name, "Developer")
        self.assertEqual(vacancy.requirements, "Python, Django")
        self.assertEqual(vacancy.salary, salary)
        self.assertEqual(vacancy.url, "http://example.com")

    def test_min_salary_greater_than_max_salary(self) -> None:
        """Тест обработки случая, когда минимальная зарплата больше максимальной."""
        with self.assertRaises(InvalidSalaryError):
            Vacancy(
                name="Developer",
                requirements="Python, Django",
                salary={"from": 3000, "to": 2000},
                url="http://example.com",
            )

    def test_negative_salary(self) -> None:
        """Тест обработки отрицательной зарплаты."""
        with self.assertRaises(InvalidSalaryError):
            Vacancy(
                name="Developer",
                requirements="Python, Django",
                salary={"from": -1000, "to": 2000},
                url="http://example.com",
            )
        with self.assertRaises(InvalidSalaryError):
            Vacancy(
                name="Developer",
                requirements="Python, Django",
                salary={"from": 1000, "to": -2000},
                url="http://example.com",
            )

    def test_vacancy_string_representation(self) -> None:
        """Тест строкового представления вакансии."""
        salary: Dict[str, Optional[int]] = {"from": 1000, "to": 2000}
        vacancy = Vacancy(name="Developer", requirements="Python, Django", salary=salary, url="http://example.com")
        expected_str = (
            "Вакансия: Developer, Требования: Python, Django, "
            "Зарплата: {'from': 1000, 'to': 2000}, Ссылка: http://example.com"
        )
        self.assertEqual(str(vacancy), expected_str)

    def test_vacancy_string_representation_no_salary(self) -> None:
        """Тест строкового представления вакансии без указания зарплаты."""
        vacancy = Vacancy(name="Developer", requirements="Python, Django", salary=None, url="http://example.com")
        expected_str = (
            "Вакансия: Developer, Требования: Python, Django, " "Зарплата: Не указана, Ссылка: http://example.com"
        )
        self.assertEqual(str(vacancy), expected_str)

    def test_vacancy_comparison(self) -> None:
        """Тест сравнения вакансий по зарплате."""
        vacancy1 = Vacancy(
            name="Junior Developer", requirements="Python", salary={"from": 1000}, url="http://example.com/junior"
        )
        vacancy2 = Vacancy(
            name="Senior Developer", requirements="Python", salary={"from": 2000}, url="http://example.com/senior"
        )

        self.assertTrue(vacancy1 < vacancy2)
        self.assertFalse(vacancy2 < vacancy1)
