import json
from typing import List

from src.models.vacancy import Vacancy
from src.storage.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    def __init__(self, filename: str = "data/vacancies.json"):
        """Инициализация экземпляра JSONStorage."""
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл."""
        vacancies = self.get_vacancies()
        if any(v.name == vacancy.name for v in vacancies):
            print(f"Вакансия с именем '{vacancy.name}' уже добавлена.")
            return
        with open(self.__filename, "a") as f:
            f.write(json.dumps(vacancy.__dict__) + "\n")

    def get_vacancies(self) -> List[Vacancy]:
        """Получает все вакансии из файла. """
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
        """Удаляет вакансию из файла. """
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.name != vacancy.name]

        with open(self.__filename, "w") as f:
            for v in vacancies:
                f.write(json.dumps(v.__dict__) + "\n")
