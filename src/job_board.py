import json
import os
from abc import ABC, abstractmethod

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv('API_KEY_SJ')


class JobBoard(ABC):
    """Абстрактный класс получения списка вакансий по API."""
    @abstractmethod
    def get_vacancies(self, search_text):
        pass


class JsonHandlerBase(ABC):
    """Абстрактный класс обработки списка вакансий."""
    @abstractmethod
    def save_vacancy(self, vacancies):
        pass

    @abstractmethod
    def get_vacancy(self, salary_from, salary_to):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class SuperJob(JobBoard):
    """Класс для работы с API SuperJob.ru"""
    def __init__(self):
        self.list_vacancies = []
        self.api_key = API_KEY

    def get_vacancies(self, search_text: str) -> list:
        """Функция для получения вакансий с SuperJob.ru."""
        url = 'https://api.superjob.ru/3.0/vacancies/'
        params = {'keyword': search_text, 'count': 100, 'page': 0}

        headers = {'X-Api-App-Id': self.api_key}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        for item in data['objects']:
            if item["payment_from"] == 0:
                continue
            elif item["payment_to"] == 0:
                continue
            else:
                vacancy = Vacancy(
                    item["profession"],
                    item["link"],
                    item["payment_from"],
                    item["payment_to"],
                    item["candidat"]
                )
                self.list_vacancies.append(vacancy)
        return self.list_vacancies


class HH(JobBoard):
    """Класс для работы с API HH.RU"""
    def __init__(self):
        self.list_vacancies = []

    def get_vacancies(self, search_text: str) -> list:
        """Функция для получения вакансий с HeadHunter.ru."""
        url = "https://api.hh.ru/vacancies"
        params = {
            'text': search_text,
            'search_field': 'name',
            'area': 1,
            'period': 1,
            'only_with_salary': True,
            'per_page': 100,
            'page': 0
        }
        response = requests.get(url, params=params)
        data = response.json()
        for item in data['items']:
            if item["salary"]["from"] == 0 or item["salary"]["from"] is None:
                continue
            elif item["salary"]["to"] == 0 or item["salary"]["to"] is None:
                continue
            else:
                vacancy = Vacancy(
                    item["name"],
                    item["alternate_url"],
                    item["salary"]["from"],
                    item["salary"]["to"],
                    item["snippet"]["responsibility"]
                )
                self.list_vacancies.append(vacancy)
        return self.list_vacancies


class Vacancy:
    """Класс для работы с вакансиями"""
    def __init__(self, name, vacancy_url, salary_from, salary_to, description):
        self.name = name
        self.vacancy_url = vacancy_url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __str__(self):
        return f"Вакансия: {self.name}\n"\
               f"Описание: {self.description}\n"\
               f"Зарплата: от {self.salary_from} до {self.salary_to}\n"\
               f"Ссылка на вакансию: {self.vacancy_url}"

    def __ge__(self, other):
        return self.salary_from >= other.salary_from

    def __le__(self, other):
        return self.salary_from <= other.salary_from

    def __eq__(self, other):
        return self.salary_from == other.salary_from

    def get_vacancy_to_dict(self):
        """Из экземпляра Vacancy получаем данные в формате словаря"""
        return {
            'name': self.name,
            'vacancy_url': self.vacancy_url,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'description': self.description
        }

    @staticmethod
    def get_vacancy_from_dict(dict_item):
        """Из формата словаря получаем экземпляр класса Vacancy"""
        return Vacancy(
            dict_item["name"],
            dict_item["vacancy_url"],
            dict_item["salary_from"],
            dict_item["salary_to"],
            dict_item["description"]
        )


class JsonHandler(JsonHandlerBase):
    """Класс для сохранения вакансии в файл json и для обработки вакансий в файле"""
    def save_vacancy(self, vacancies):
        """Функция для сохранения в файл"""
        list_vacancies = []
        for vacancy in vacancies:
            list_vacancies.append(vacancy.get_vacancy_to_dict())

        with open("../data/vacancies.json", 'w') as f:
            json.dump(list_vacancies, f, ensure_ascii=False, indent=4)

    def get_vacancy(self, salary_from: int, salary_to: int) -> list:
        """Функция фильтрует вакансии по указанной зарплате и выдает пользователю"""
        list_vacancies_by_salary = []

        with open("../data/vacancies.json", 'r') as f:
            list_vacancies = json.load(f)
        for vacancy in list_vacancies:
            if vacancy["salary_from"] >= salary_from and vacancy["salary_to"] <= salary_to:
                list_vacancies_by_salary.append(Vacancy.get_vacancy_from_dict(vacancy))

        return list_vacancies_by_salary

    def delete_vacancy(self):
        os.system(r' >../data/vacancies.json')


# дополнительная функция для фильтрации вакансий
def get_vacancies_by_description(vacancies: list, text: str) -> list:
    """Функция фильтрации вакансий по переданному слову, которое содержится в описании вакансии.
    :param vacancies: список словарей с вакансиями
    :param text: значение для поиска в описании вакансии
    :return: список
    """

    result_list = [item for item in vacancies if text in item.description]
    return result_list
