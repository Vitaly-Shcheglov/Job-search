from pathlib import Path
from typing import Generator

import pytest

from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


@pytest.fixture
def json_storage(tmp_path: Path) -> Generator[JSONStorage, None, None]:
    """Создает временное хранилище для вакансий."""
    temp_file = tmp_path / "vacancies.json"
    storage = JSONStorage(str(temp_file))
    yield storage
    # Удаление временного файла не требуется, так как pytest автоматически очистит tmp_path


def test_add_vacancy(json_storage: JSONStorage) -> None:
    """Тест добавления вакансии."""
    vacancy = Vacancy(
        name="Developer",
        salary={"from": 1000, "to": 2000},  # Убедитесь, что salary – это словарь
        requirements="Python, Django",
        url="https://api.hh.ru/vacancies",
    )
    json_storage.add_vacancy(vacancy)

    # Проверяем, что вакансия добавилась
    vacancies = json_storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].name == "Developer"


def test_add_duplicate_vacancy(json_storage: JSONStorage) -> None:
    """Тест добавления дубликата вакансии."""
    vacancy = Vacancy(
        name="Developer",
        salary={"from": 1000, "to": 2000},
        requirements="Python, Django",
        url="https://api.hh.ru/vacancies",
    )
    json_storage.add_vacancy(vacancy)

    # Пытаемся добавить дубликат
    json_storage.add_vacancy(vacancy)

    # Проверяем, что вакансия не добавилась второй раз
    vacancies = json_storage.get_vacancies()
    assert len(vacancies) == 1


def test_delete_vacancy(json_storage: JSONStorage) -> None:
    """Тест удаления вакансии."""
    vacancy = Vacancy(
        name="Developer",
        salary={"from": 1000, "to": 2000},
        requirements="Python, Django",
        url="https://api.hh.ru/vacancies",
    )
    json_storage.add_vacancy(vacancy)

    # Удаляем вакансию
    json_storage.delete_vacancy(vacancy)

    # Проверяем, что вакансий больше нет
    vacancies = json_storage.get_vacancies()
    assert len(vacancies) == 0


def test_get_vacancies_empty(json_storage: JSONStorage) -> None:
    """Тест получения пустого списка вакансий."""
    # Если файл пустой, должны получать пустой список
    vacancies = json_storage.get_vacancies()
    assert vacancies == []
