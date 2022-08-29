# search_profiles
Производит поиск по сайтам, и смотрит, зарегистрирован ли пользователь с ником "user_name"


search_profile.py
Последовательно переходит по ссылкам
Выводит положительные результаты на экран. Сохраняет все данные в .json файл

search_profile_multiprocess.py
Используя модуль "multiprogress" переходит по ссылкам. В несколько раз быстрее чем search_profile.py
Выводит положительные результаты на экран. Сохраняет все данные в .csv файл


Можно использовать как полноценную программу.

Первый способ - указать аргументы при запуске программы через консоль
python search_profile.py user1 user2 user3
python search_profile_multiprocess.py user1 user3 user3

Второй способ - ввести аргументы после запуска программы
python search_profile.py
$/> user1 user2 user3


Можно использовать как отдельный модуль
from search_profile import search_profile
from search_profile_multiprocess import search_profile_multiprocess
