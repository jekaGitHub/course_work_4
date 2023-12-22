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


class JsonHandler(ABC):
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
    def __init__(self):
        self.list_vacancies = []
        self.api_key = API_KEY

    def get_vacancies(self, search_text):
        url = 'https://api.superjob.ru/3.0/vacancies/'
        params = {'keyword': search_text, 'count': 100, 'page': 0}

        headers = {'X-Api-App-Id': self.api_key}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        self.list_vacancies.append(data['objects'])
        return self.list_vacancies


class HH(JobBoard):
    def __init__(self):
        self.list_vacancies = []

    def get_vacancies(self, search_text):
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
        self.list_vacancies.append(data['items'])
        return self.list_vacancies


class Vacancy:
    def __init__(self, name, vacancy_url, salary_from, salary_to, description):
        self.name = name
        self.vacancy_url = vacancy_url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __gt__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __eq__(self, other):
        pass
