from typing import Generator, List
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies, user_interaction


@pytest.fixture
def mock_hh_api() -> Generator[Mock, None, None]:
    with patch.object(HeadHunterAPI, "get_vacancies", return_value=...) as mock:
        yield mock


@pytest.fixture
def mock_storage() -> Generator[Mock, None, None]:
    with patch.object(JSONStorage, "add_vacancy", return_value=...) as mock:
        yield mock


def test_user_interaction(mock_hh_api: MagicMock, mock_storage: MagicMock) -> None:
    mock_hh_api.return_value = [
        {
            "name": "Developer",
            "snippet": {"requirement": "Python"},
            "salary": {"from": 120000},
            "alternate_url": "https://api.hh.ru/vacancies",
        },
        {
            "name": "Designer",
            "snippet": {"requirement": "Photoshop"},
            "salary": {"from": 80000},
            "alternate_url": "https://api.hh.ru/vacancies",
        },
    ]

    with patch("builtins.input", side_effect=["Developer", 5, "Python", "100000-150000"]):
        user_interaction()

    assert mock_storage.call_count == 2


def test_get_vacancies_by_salary() -> None:
    vacancies: List[Vacancy] = [
        Vacancy(name="Developer", salary={"from": 120000}, requirements="Python", url="https://api.hh.ru/vacancies"),
        Vacancy(name="Designer", salary={"from": 80000}, requirements="Photoshop", url="https://api.hh.ru/vacancies"),
    ]
    salary_range: str = "100000-130000"
    filtered_vacancies = get_vacancies_by_salary(vacancies, salary_range)

    assert len(filtered_vacancies) == 0


def test_filter_vacancies() -> None:
    vacancies: List[Vacancy] = [
        Vacancy(
            name="Developer",
            salary={"from": 1000, "to": 2000},
            requirements="Python, Django",
            url="https://api.hh.ru/vacancies",
        ),
        Vacancy(
            name="Designer",
            salary={"from": 800, "to": 1200},
            requirements="Photoshop",
            url="https://api.hh.ru/vacancies",
        ),
    ]
    keywords: List[str] = ["python"]
    filtered: List[Vacancy] = filter_vacancies(vacancies, keywords)

    assert len(filtered) == 1
    assert filtered[0].name == "Developer"


def test_sort_vacancies() -> None:
    vacancies: List[Vacancy] = [
        Vacancy(name="Developer", salary={"from": 120000}, requirements="Python", url="https://api.hh.ru/vacancies"),
        Vacancy(name="Designer", salary={"from": 80000}, requirements="Photoshop", url="https://api.hh.ru/vacancies"),
    ]
    sorted_vacancies: List[Vacancy] = sort_vacancies(vacancies)

    assert sorted_vacancies[0].name == "Developer"
    assert sorted_vacancies[1].name == "Designer"


def test_get_top_vacancies() -> None:
    vacancies: List[Vacancy] = [
        Vacancy(name="Developer", salary={"from": 120000}, requirements="Python", url="https://api.hh.ru/vacancies"),
        Vacancy(name="Designer", salary={"from": 80000}, requirements="Photoshop", url="https://api.hh.ru/vacancies"),
    ]
    top_vacancies: List[Vacancy] = get_top_vacancies(vacancies, 1)

    assert len(top_vacancies) == 1
    assert top_vacancies[0].name == "Developer"
