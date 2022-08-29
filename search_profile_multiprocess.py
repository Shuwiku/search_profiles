from art import tprint
from argparse import ArgumentParser
from json import load
from requests import get as req_get, exceptions as req_exceptions
from multiprocessing import Pool
from os.path import isfile
from time import time


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


def logging(data):
    file_name = f'search_profile_multiprocess_{data[1]}.csv'
    if not isfile(file_name):
        string = ';'.join(['Social', 'User Name', 'Status Code', 'Status Message', 'URL']) + '\n'
        with open(file_name, mode='w', encoding='utf-8') as f:
            f.write(string)

    string = '\n' + ';'.join(data)
    with open(file_name, mode='a', encoding='utf-8') as f:
        f.write(string)


def make_request(data):
    global STATUS_CODES

    user_name, social, url = data
    url = url.replace('{user_name}', user_name)

    try:
        request = req_get(url)
        status = str(request.status_code)
    except req_exceptions.TooManyRedirects:
        status = 'Too many redirects'
    except req_exceptions.ConnectionError:
        status = 'Connection error'
    except req_exceptions.Timeout:
        status = 'Timeout'

    message = STATUS_CODES[status]
    user_data = [social, user_name, status, message, url]

    if status == '200':
        print(f'[{message}] {social} -> {url}')

    logging(user_data)


def search(user_name, links_path):
    links = load(open(links_path, mode='r', encoding='utf-8'))

    iterations = 1
    links_len = len(list(links.keys()))
    for i in range(0, links_len, 60):
        iteration = list(links.items())[i:iterations * 60]
        iteration_data = []
        for j in iteration:
            iteration_data.append((user_name, *j))
        pool = Pool(processes=len(iteration_data))
        pool.map(make_request, iteration_data)
        iterations += 1


def search_profile_multiprocess(user_names_list: list, links_path='links.json'):
    if len(user_names_list) == 0:
        help_message_text = 'Please, input user names\n' \
                            'For example: $/> shuwiku shiro bettapy'
        print(help_message_text)
        user_names_list = input('$/> ').split()

    for user_name in user_names_list:
        time_a = time()
        print(f'A search is in progress for "{user_name}". This may take some time. Please wait')
        search(user_name, links_path)
        time_b = time()
        print(f'Saved in "search_profile_multiprocess_{user_name}.csv"')
        print(f'Total time: {time_b - time_a}')


if __name__ == '__main__':
    tprint('search-profile', font='ogre')
    tprint('multiprocess')
    print('by shuwiku\nGitHub: https://github.com/Shuwiku\n\n')

    parser = ArgumentParser()
    help_message = 'Input user names "python search_profiles u [user_1] [user_2] [user_3]"' \
                   'For example: "python search_profiles u shuwiku shiro bettapy"'
    parser.add_argument('users', nargs='*', help=help_message)
    user_names_args = parser.parse_args().users

    search_profile_multiprocess(user_names_args)
