import unittest
from typing import Dict

from exceptions import InvalidSalaryError
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


class TestVacancy(unittest.TestCase):

    def test_create_vacancy_valid_salary(self) -> None:
        valid_salary: Dict[str, int] = {"from": 50000, "to": 70000}
        vacancy = Vacancy("Software Engineer", "Python, SQL", valid_salary, "http://example.com")
        self.assertEqual(vacancy.name, "Software Engineer")
        self.assertEqual(vacancy.requirements, "Python, SQL")
        self.assertEqual(vacancy.salary, valid_salary)
        self.assertEqual(vacancy.url, "http://example.com")

    def test_create_vacancy_negative_salary(self) -> None:
        with self.assertRaises(InvalidSalaryError):
            Vacancy("Software Engineer", "Python, SQL", {"from": -50000, "to": 70000}, "http://example.com")

    def test_create_vacancy_from_greater_than_to(self) -> None:
        with self.assertRaises(InvalidSalaryError):
            Vacancy("Software Engineer", "Python, SQL", {"from": 70000, "to": 50000}, "http://example.com")

    def test_create_vacancy_invalid_salary_format(self) -> None:
        with self.assertRaises(InvalidSalaryError):
            Vacancy("Software Engineer", "Python, SQL", "invalid_salary", "http://example.com")

    def test_compare_vacancies(self) -> None:
        vacancy1 = Vacancy(
            "Junior Developer", "Basic knowledge of Python", {"from": 30000, "to": 40000}, "http://example.com/1"
        )
        vacancy2 = Vacancy(
            "Senior Developer", "Expert knowledge of Python", {"from": 60000, "to": 80000}, "http://example.com/2"
        )
        self.assertTrue(vacancy1 < vacancy2)

    def test_str_representation(self) -> None:
        vacancy = Vacancy("Software Engineer", "Python, SQL", {"from": 50000, "to": 70000}, "http://example.com")
        expected_str = (
            "Вакансия: Software Engineer, Требования: Python, SQL,"
            " Зарплата: {'from': 50000, 'to': 70000}, Ссылка: http://example.com"
        )
        self.assertEqual(str(vacancy), expected_str)
