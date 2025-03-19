from typing import Any, Dict, List, Optional

from src.api.hh_api import HeadHunterAPI
from exceptions import InvalidSalaryError, VacancyNotFoundError, ZeroQuantityError
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str], salary_range: Optional[str]) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам и диапазону зарплат."""
    filtered_vacancies: List[Vacancy] = []

    # Распределяем диапазон зарплат
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    if salary_range:
        try:
            min_salary, max_salary = map(int, salary_range.split("-"))
        except ValueError:
            raise InvalidSalaryError("Некорректный диапазон зарплат. Используйте формат: 'мин - макс'")

    for vacancy in vacancies:
        # Проверка на наличие ключевых слов в описании вакансии
        if any(word.lower() in vacancy.name.lower() for word in filter_words):
            # Проверка на соответствие диапазону зарплат
            if vacancy.salary is not None:
                salary = vacancy.salary["from"] if vacancy.salary["from"] is not None else 0
                if (min_salary is None or salary >= min_salary) and (max_salary is None or salary <= max_salary):
                    filtered_vacancies.append(vacancy)
            else:
                filtered_vacancies.append(vacancy)

    return filtered_vacancies


def user_interaction() -> None:
    """Взаимодействует с пользователем для получения и фильтрации вакансий."""
    hh_api = HeadHunterAPI()  # Создаем экземпляр API
    search_query: str = input("Введите поисковый запрос: ")
    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range: str = input("Введите диапазон зарплат (пример: 100000 - 150000): ")  # Пример: 100000 - 150000

    try:
        vacancies_data: List[Dict[str, Any]] = hh_api.get_vacancies(search_query)  # Получаем вакансии
        vacancies_list: List[Vacancy] = []

        for item in vacancies_data:
            vacancy = Vacancy(
                item["name"],
                item["snippet"]["requirement"],
                item.get("salary", None),  # Используем None, если зарплата не указана
                item["alternate_url"],
            )
            vacancies_list.append(vacancy)

        # Фильтруем вакансии
        filtered_vacancies = filter_vacancies(vacancies_list, filter_words, salary_range)

        # Ограничиваем вывод по количеству
        top_vacancies = filtered_vacancies[:top_n]

        if top_vacancies:
            for vacancy in top_vacancies:
                print(vacancy)
        else:
            print("Нет подходящих вакансий по заданным критериям.")

    except VacancyNotFoundError as e:
        print(e)  # Выводим сообщение об ошибке, если вакансии не найдены
    except InvalidSalaryError as e:
        print(e)  # Обработка ошибок, связанных с зарплатой
    except ZeroQuantityError as e:
        print(e)  # Обработка ошибок, связанных с количеством
    except Exception as e:
        print(f"Произошла ошибка: {e}")  # Обработка всех остальных ошибок


if __name__ == "__main__":
    user_interaction()  # Запускаем функцию взаимодействия с пользователем
