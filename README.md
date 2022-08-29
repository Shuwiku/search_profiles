# search_profiles
Производит поиск по сайтам, и смотрит, зарегистрирован ли пользователь с ником "user_name"


<h3>search_profile.py</h3>
Последовательно переходит по ссылкам<br>
Выводит положительные результаты на экран. Сохраняет все данные в .json файл<br>
<br>
<h3>search_profile_multiprocess.py</h3>
Используя модуль "multiprogress" переходит по ссылкам. В несколько раз быстрее чем search_profile.py<br>
Выводит положительные результаты на экран. Сохраняет все данные в .csv файл<br>
<br>
<br>
Можно использовать как полноценную программу.<br>
<br>
<b>Первый способ</b> - указать аргументы при запуске программы через консоль<br>
<i>python search_profile.py user1 user2 user3</i><br>
<i>python search_profile_multiprocess.py user1 user3 user3</i><br>
<br>
<b>Второй способ</b> - ввести аргументы после запуска программы<br>
<i>python search_profile.py</i><br>
<i>$/> user1 user2 user3</i><br>
<br>
<br>
Можно использовать как отдельный модуль<br>
<i>from search_profile import search_profile</i><br>
<i>from search_profile_multiprocess import search_profile_multiprocess</i><br>
