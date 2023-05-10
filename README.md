# django-friends
## _Сервис для друзей Вконтакте_

## Основные функции

- Зарегистрировать пользователя
- Отправить заявку в друзья, просмотреть статус пользователя, отклонить/принять заявку
- Вывести список друзей
- Посмотреть свои заявки и входящие заявки в друзья

## _Стек:_

- PostrgeSQL, DRF

### Развертка репозитория на локальном сервере:

1. Клонировать репозиторий себе на локальную машину
```sh
git clone https://github.com/KazakNi/django-friends
```
2. Перейти в папку с проектом.
```sh
cd django-friends
```
3. Развернуть виртуальное окружение, установить зависимости, заполнить файл с переменными окружения, выполнить первичные миграции и запустить приложение.
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
4. Redoc документация будет доступна по адресу: http://127.0.0.1:8000/redoc/


### Пример запроса на эндпоинт /api/auth/users/:

Отправляем POST-запрос с такими данными:
```sh
{
    "email": "coder.love@vk.ru",
    "password": "intern123",
    "username": "Chance"
}
```
Ответ сервера:

![](https://sun9-78.userapi.com/impg/ZxlVN49P_YD9AW2MEcRl2sBYXOZogZTJBDEagw/EBf-Sl5eLcw.jpg?size=151x25&quality=95&sign=f5ae659630fff80206d9a1d9b7078210&type=album)

Пользователь создан. Получив токен по адресу /api/auth/token/login/, можно далее пользоваться сервисом.
