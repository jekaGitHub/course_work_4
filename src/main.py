from src.job_board import SuperJob, HH, Vacancy, JsonHandler


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("Добро пожаловать!")
    platforms = {"1": "HeadHunter", "2": "SuperJob"}
    list_vacancies = []

    user_input = input("Введите цифру 1, если хотите получить вакансии с сайта HeadHunter.\n"
                       "Введите цифру 2, если хотите получить вакансии с сайта SuperJob.")
    if user_input == '1' or user_input == '2':
        vacancy_name = input("Введите название профессии для поиска вакансий на сайте:\n")
        if user_input == '1':
            hh_api = HH()
            list_vacancies = hh_api.get_vacancies(vacancy_name)
        elif user_input == '2':
            superjob_api = SuperJob()
            list_vacancies = superjob_api.get_vacancies(vacancy_name)

        if len(list_vacancies) == 0:
            print(f"Вакансий по профессии {vacancy_name} на сайте {platforms[user_input]} не найдено!")
        else:
            json_saver = JsonHandler()
            json_saver.save_vacancy(list_vacancies)
            print(f"Список вакансий на сайте {platforms[user_input]} по профессии {vacancy_name}:\n")
            for vacancy in list_vacancies:
                print(vacancy)

            vacancy_salary = input("Хотите отфильтровать вакансии по зарплате? Введите 'да' или 'нет'\n")
            if vacancy_salary.lower() == "да":
                salary_from = int(input("Введите минимальную зарплату:\n"))
                salary_to = int(input("Введите максимальную зарплату:\n"))
                vacancies = json_saver.get_vacancy(salary_from, salary_to)
                if vacancies is None:
                    print(f"Нет вакансий с зарплатой от {salary_from} до {salary_to} рублей.")
                else:
                    for vacancy in vacancies:
                        print(vacancy)
    else:
        print("Вы не выбрали сайт или ввели значение, которого нет. Попробуйте снова!")


if __name__ == '__main__':
    user_interaction()
    # sj = SuperJob()
    # print(sj.get_vacancies("PHP"))

    # hh = HH()
    # print(hh.get_vacancies("Python"))
