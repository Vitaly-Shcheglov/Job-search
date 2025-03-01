from typing import List

from src.api.hh_api import HeadHunterAPI
from src.exceptions import VacancyNotFoundError
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


def user_interaction() -> None:
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    search_query: str = input("Введите поисковый запрос: ")
    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range: str = input("Введите диапазон зарплат (например: 100000 - 150000): ")

    try:
        vacancies_data = hh_api.get_vacancies(search_query)
        vacancies_list: List[Vacancy] = []

        for item in vacancies_data:
            vacancy = Vacancy(
                item["name"],
                item["snippet"]["requirement"],
                item.get("salary", 0),
                item["alternate_url"],
            )
            vacancies_list.append(vacancy)
            storage.add_vacancy(vacancy)

        filtered_vacancies: List[Vacancy] = filter_vacancies(vacancies_list, filter_words)
        ranged_vacancies: List[Vacancy] = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies: List[Vacancy] = sort_vacancies(ranged_vacancies)
        top_vacancies: List[Vacancy] = get_top_vacancies(sorted_vacancies, top_n)

        print_vacancies(top_vacancies)

    except VacancyNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам."""
    filtered_vacancies: List[Vacancy] = []
    for vacancy in vacancies:
        if any(keyword.lower() in vacancy.requirements.lower() for keyword in keywords):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрует вакансии по указанному диапазону зарплат."""
    min_salary, max_salary = map(int, salary_range.split("-"))
    ranged_vacancies: List[Vacancy] = [
        vacancy
        for vacancy in vacancies
        if isinstance(vacancy.salary, int) and min_salary <= vacancy.salary <= max_salary
    ]
    return ranged_vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате."""
    return sorted(vacancies, key=lambda v: v.salary if isinstance(v.salary, int) else float("-inf"), reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ N вакансий."""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит вакансии на экран."""
    for vacancy in vacancies:
        print(vacancy)
