import os
from abc import ABC, abstractmethod

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv('API_KEY_SJ')


class JobBoard(ABC):
    @abstractmethod
    def get_vacancies(self, search_text):
        pass


class JsonHandlerBase(ABC):
    @abstractmethod
    def save_vacancy(self):
        pass

    @abstractmethod
    def get_vacancy(self):
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
        return f"Вакансия: {self.name}"\
               f"Описание: {self.description}"\
               f"Зарплата: от {self.salary_from} до {self.salary_to}"\
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
    def save_vacancy(self):
        pass

    def get_vacancy(self):
        pass

    def delete_vacancy(self):
        pass
