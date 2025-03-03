import json
from typing import List

from src.models.vacancy import Vacancy
from src.storage.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    """Класс для работы с вакансиями, хранящимися в формате JSON.

    Этот класс наследует от BaseStorage и реализует методы для добавления,
    получения и удаления вакансий, хранящихся в JSON-файле.
    """

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """Инициализация экземпляра JSONStorage.

        Аргументы:
            filename (str): Имя файла, в который будут сохраняться вакансии.
        """
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл.

        Аргументы:
            vacancy (Vacancy): Объект вакансии, который нужно добавить в файл.

        Если вакансия с таким же именем уже существует, она не будет добавлена.
        """
        vacancies = self.get_vacancies()
        if any(v.name == vacancy.name for v in vacancies):
            print(f"Вакансия с именем '{vacancy.name}' уже добавлена.")
            return
        with open(self.__filename, "a") as f:
            # Предполагается, что у Vacancy есть атрибуты name, requirements, url и salary.
            vacancy_data = {
                "name": vacancy.name,
                "requirements": vacancy.requirements,
                "url": vacancy.url,
                "salary": vacancy.salary,
                # добавьте другие атрибуты по мере необходимости
            }
            f.write(json.dumps(vacancy_data) + "\n")

    def get_vacancies(self) -> List[Vacancy]:
        """Получает все вакансии из файла.

        Возвращает:
            List[Vacancy]: Список объектов вакансий, загруженных из файла.
            Если файл не найден, возвращается пустой список.
        """
        vacancies = []
        try:
            with open(self.__filename, "r") as f:
                for line in f:
                    vacancy_data = json.loads(line)
                    vacancies.append(Vacancy(**vacancy_data))
        except FileNotFoundError:
            print("Файл не найден, возвращаем пустой список.")
        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из файла.

        Аргументы:
            vacancy (Vacancy): Объект вакансии, который нужно удалить из файла.
        """
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.name != vacancy.name]

        with open(self.__filename, "w") as f:
            for v in vacancies:
                vacancy_data = {
                    "name": v.name,
                    "requirements": v.requirements,
                    "url": v.url,
                    "salary": v.salary,
                    # добавьте другие атрибуты по мере необходимости
                }
                f.write(json.dumps(vacancy_data) + "\n")
