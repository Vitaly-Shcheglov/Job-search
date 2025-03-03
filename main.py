from typing import Any, Dict, List, Optional

from exceptions import InvalidSalaryError, VacancyNotFoundError, ZeroQuantityError
from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str], salary_range: Optional[str]) -> List[Vacancy]:
    filtered_vacancies: List[Vacancy] = []

    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    if salary_range:
        try:
            min_salary, max_salary = map(int, salary_range.split("-"))
        except ValueError:
            raise InvalidSalaryError("Некорректный диапазон зарплат. Используйте формат: 'мин - макс'")

    for vacancy in vacancies:
        if any(word.lower() in vacancy.name.lower() for word in filter_words):
            if vacancy.salary is not None:
                salary = vacancy.salary["from"] if vacancy.salary["from"] is not None else 0
                if (min_salary is None or salary >= min_salary) and (max_salary is None or salary <= max_salary):
                    filtered_vacancies.append(vacancy)
            else:
                filtered_vacancies.append(vacancy)

    return filtered_vacancies


def user_interaction() -> None:
    hh_api = HeadHunterAPI()
    search_query: str = input("Введите поисковый запрос: ")
    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range: str = input("Введите диапазон зарплат (пример: 100000 - 150000): ")

    try:
        vacancies_data: List[Dict[str, Any]] = hh_api.get_vacancies(search_query)
        vacancies_list: List[Vacancy] = []

        for item in vacancies_data:
            vacancy = Vacancy(
                item["name"],
                item["snippet"]["requirement"],
                item.get("salary", None),
                item["alternate_url"],
            )
            vacancies_list.append(vacancy)

        filtered_vacancies = filter_vacancies(vacancies_list, filter_words, salary_range)

        top_vacancies = filtered_vacancies[:top_n]

        if top_vacancies:
            for vacancy in top_vacancies:
                print(vacancy)
        else:
            print("Нет подходящих вакансий по заданным критериям.")

    except VacancyNotFoundError as e:
        print(e)
    except InvalidSalaryError as e:
        print(e)
    except ZeroQuantityError as e:
        print(e)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    user_interaction()
