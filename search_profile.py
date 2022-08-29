from argparse import ArgumentParser
from json import load, dump
from time import time

from art import tprint
from progress.bar import ChargingBar
from requests import get as req_get, exceptions as req_exceptions


STATUS_CODES = {
    "100": "Continue", "101": "Switching protocols", "102": "Processing",
    "103": "Early Hints ", "200": "OK", "201": "Created", "202": "Accepted",
    "203": "Non-Authoritative Information", "204": "No Content", "205": "Reset Content",
    "206": "Partial Content", "207": "Multi-Status", "208": "Already Reported",
    "226": "IM Used", "300": "Multiple Choices", "301": "Moved Permanently",
    "302": "Found", "303": "See Other", "304": "Not Modified",
    "305": "Use Proxy", "306": "Switch Proxy", "307": "Temporary Redirect",
    "308": "Permanent Redirect", "400": "Bad Request", "401": "Unauthorized",
    "402": "Payment Required", "403": "Forbidden", "404": "Not Found",
    "405": "Method Not Allowed", "406": "Not Acceptable", "407": "Proxy Authentication Required",
    "408": "Request Timeout", "409": "Conflict", "410": "Gone",
    "411": "Length Required", "412": "Precondition Failed", "413": "Payload Too Large",
    "414": "URI Too Long", "415": "Unsupported Media Type", "416": "Range Not Satisfiable",
    "417": "Expectation Failed", "418": "I'm a Teapot", "421": "Misdirected Request",
    "422": "Unprocessable Entity", "423": "Locked", "424": "Failed Dependency",
    "425": "Too Early", "426": "Upgrade Required", "428": "Precondition Required",
    "429": "Too Many Requests", "431": "Request Header Fields Too Large",
    "451": "Unavailable For Legal Reasons", "500": "Internal Server Error",
    "501": "Not Implemented", "502": "Bad Gateway", "503": "Service Unavailable",
    "504": "Gateway Timeout", "505": "HTTP Version Not Supported", "506": "Variant Also Negotiates",
    "507": "Insufficient Storage", "508": "Loop Detected", "510": "Not Extended",
    "511": "Network Authentication Required", "Too many redirects": "Too many redirects",
    "Connection error": "Connection error", "Timeout": "Timeout"
}


def make_request(url):
    try:
        request = req_get(url)  # Запрос
        status = str(request.status_code)  # Код (200 / 404 / etc)
    except req_exceptions.TooManyRedirects:
        status = 'Too many redirects'
    except req_exceptions.ConnectionError:
        status = 'Connection error'
    except req_exceptions.Timeout:
        status = 'Timeout'
    return status


def search(user_name, links_path):
    global STATUS_CODES

    links = load(open(links_path, mode='r', encoding='utf-8'))  # Ссылки на сайты

    bar = ChargingBar(user_name, max=len(list(links.keys())))  # Прогресс-Бар
    search_result = {}  # Данные по всем запросам. Сохраняется в .json
    status_code_200 = []  # Данные по положительным запросам (status=200). Выводится в консоль
    for site_name in list(links.keys()):  # Проходимся по всем ссылкам на сайты
        url = links[site_name].replace('{user_name}', user_name)  # Ссылка на профиль
        status = make_request(url)  # Получаем код
        message = STATUS_CODES[status]  # Расшифровываем код

        search_result[site_name] = {  # Форма для добавления в .json
            "user_name": user_name,
            "status_code": [status, message],
            "url": url
        }
        bar.next()  # Двигаем Прогресс-Бар

        if status == '200':  # Если запрос положительный, добавляем в список, который потом
            status_code_200.append(f'[{message}] {site_name} -> {url}')  # выведется в консоль

    bar.finish()  # Завершаем работу Прогресс-Бара
    for result in status_code_200:  # Выводим положительные запросы
        print(result)

    return search_result


def search_profile(user_names_list: list, save_file_name='', links_path='links.json'):
    if len(user_names_list) == 0:  # Если не заданы параметры "python search_profile.py user1 user2"
        help_message_text = 'Please, input user names\n' \
                            'For example: $/> shuwiku shiro bettapy'
        print(help_message_text)
        user_names_list = input('$/> ').split()

    for user_name in user_names_list:
        time_a = time()
        search_result = search(user_name, links_path)  # Сам процесс поиска

        save_path = f'{save_file_name}search_profile_{user_name}.json'
        print(f'Saving in "{save_path}"')
        with open(save_path, mode='w', encoding='utf-8') as user_file:  # Сохранение в .json
            dump(search_result, user_file, indent=4)
        print('Saved successfully.')
        time_b = time()
        print(f'Total time: {time_b - time_a}\n')


if __name__ == '__main__':
    tprint('search-profile', font='ogre')  # Крутое лого
    print('by shuwiku\nGitHub: https://github.com/Shuwiku\n\n')

    parser = ArgumentParser()  # Парсер аргументов
    help_message = 'Input user names "python search_profiles u [user_1] [user_2] [user_3]"' \
                   'For example: "python search_profiles u shuwiku shiro bettapy"'
    parser.add_argument('users', nargs='*', help=help_message)
    user_names_args = parser.parse_args().users

    search_profile(user_names_args)
