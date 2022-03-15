# PAKT Work Tools
Комплекс инструментов для работы с петрозаводским аннотированным корпусом

## Возможности
### Аннотирование корпуса
* Преподаватель
  * Загрузка работ от лица студента
  * Просмотр и удаление любых работ
  * ~~Аннтирование всех текстов~~
  * ~~Возможность давать доступ студентам для аннотирования текста~~

* Студент
  * Загрузка новых работ от своего лица
  * Просмотр и удаление только своих работ
  * ~~Аннотация только разрешенных текстов~~


### Поиск по корпусу
РАЗРАБОТКА


## Установка
**Пре-установка**
1. Установите [GIT](https://git-scm.com/downloads)
2. Установите [Python3](https://www.python.org/downloads/)


**Установка**
1. Создайте папку для проекта
2. Установите виртуальное окружение
`
pip install virtualenv
`
3. Создайте виртуальное окружение pakt
`
python -m venv pakt
`
4. Запустите виртуальное окружение
Для Windows:
`
.\pakt\Scripts\Activate.ps1
`
5. Склонируйте проект с git
`
git clone https://github.com/remshu/pakt-work-tools.git
`
и перейдите в папку
6. Установите все требуемые библиотеки
`
pip install -r requirements.txt
`
7. Создайте миграцию
`
python manage.py makemigrations
`
7. Запустите миграцию
`
python manage.py migrate
`
7. Запустите сервер
`
python manage.py runserver
`
