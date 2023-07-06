# PAKT Work Tools
Комплекс инструментов (библиотека) для работы с петрозаводским аннотированным корпусом.

## Цель и миссия
Библиотека предназначена для накопления корпуса ученических текстов, аннотирования текстов
и определения степени грубости ошибки и выставления общей оценки за ученический текст
на немецком языке, исходя из настраиваемой шкалы оценивания.
Библиотека реализует функции, которые традиционно выполняются преподавателем:
интерпретация лингвистических ошибок в тексте обучающегося на предмет ее грубости и обобщение результатов в виде общей оценки за весь текст.  

Разработанная библиотека может быть использована для:
1. Создания информационных систем автоматизации деятельности преподавателей иностранных языков;
2. Проведения научных исследований в области аттестации обучающихся иностранному языку.

В частности, библиотека была использована участниками для подготовки статьи “Котюрова И.А. Корпус студенческих текстов на немецком языке как источник данных для образования и науки [Текст] / И.А. Котюрова, Л.В. Щеголева // Вопросы образования. - Москва, 2022. - №4. - С.322-349. - Режим доступа: https://vo.hse.ru/article/view/16526/15535”.

## Возможности
### Аннотирование корпуса
Загрузка текстов и аннотирование выполняется через веб интерфейс инструментария.

* Возможности преподавателя
  * Загрузка работ от лица студента
  * Просмотр и удаление любых работ
  * Аннтирование всех текстов
  * ~~Возможность давать доступ студентам для аннотирования текста~~

* Возможности студента
  * Загрузка новых работ от своего лица
  * Просмотр и удаление только своих работ
  * ~~Аннотация только разрешенных текстов~~

Инструкция по установки и настройке инструментария описана в разделе [Установка](#установка).
Инструкция по работе с веб интерфейсом аннотирования корпуса описана в [docs/guide.md](docs/guide.md).


### Поиск по корпусу
Модуль search_app предоставляет пользователю интерфейс для поиска по корпусу с использованием языка [Corpus Query Language](https://www.sketchengine.eu/documentation/corpus-querying/).
Документация по поиску размещена в файле [docs/cql.md](docs/cql.md). 

### Выгрузка корпуса
Документация и скрипты для выгрузки корпуса размещены в [каталоге модуля](csv-dump).
Текущая версия выгруженного корпуса размещена в [Hugging Face](https://huggingface.co/datasets/remshu-inc/marks).

### Модуль построения оценок
Документация и скрипты обучения и использования модуля построения оценок размещены в [каталоге модуля](grading_module).

___
## __Установка__
### Подготовка
### Выгрузка предобученных моделей
Документация и примеры скриптов выгрузки предобученных моделей размещены в [каталоге модуля построения оценок](grading_module).
Текущая версия предобученной модели определения грубости ошибки размещена в [Hugging Face](https://huggingface.co/remshu-inc/mencoder).
Текущая версия предобученной модели оценки текста размещена в [Hugging Face](https://huggingface.co/remshu-inc/mencoder).

## Системные требования
Для запуска библиотеки требуется ЭВМ с 64-битной архитектурой и установленным
интерпретатором языка Python версии не ниже 3.9.
Обучение нейронных сетей выполняется с помощью библиотек Torch и Tensorflow и
требует не менее 10Гб ОЗУ или использования соответствующих графических видеоускорителей.
Для использования библиотеки с обученными нейронными сетями требуется ЭВМ с 64-битной
архитектурой н не менее 8Гб ОЗУ.

## Установка
**Пре-установка**
1. Установите [GIT](https://git-scm.com/downloads)
2. Установите [Python3](https://www.python.org/downloads/)
3. Установите и настройте [MySQL Server ](https://dev.mysql.com/downloads/mysql/) или [MariaDB](https://mariadb.org/download/)
	
	1. В системе _PAKT_, по умолчанию используются стандартные настройки подключения к _MySQL_/_MariaDB_. В случае их изменения - внесите корректировки в соответсвующие настройки сервиса (см. раздел `Установка` - `п. 2.5`).
	2. Обязательно запомните пароль для `root` пользователя созданного при установке выбранной СУБД.


### Установка
1. __Разворачивание системы__
	1. Создайте папку для проекта
	2. Создайте виртуальное окружение:

		> python -m venv pakt

	3. Запустите виртуальное окружение:
		
		1. Linux:
			> source .\pakt\bin\activate

		2. Windows (PowerShell):
			> .\pakt/scripts/Activate.ps1
	4. Склонируйте код проекта из репозитория:
		> git clone `https://github.com/remshu/pakt-work-tools.git`	
	5. Перейдите в появившуюся папку `pakt-work-tools`
	6. Установите все требуемые библиотеки для _Python_:
		> pip install  -r requirements.txt 

	7. Создайте необходимые директории:
		> python create_folders.py
2. __Создание базы данных и подключение__

	(_используемые команды и методы работают как с MySQL, так и с MariaDB_)
	1. Перейдите в консоль взаимодействия с СУБД 
		
		1. MySQL CommandLine - 
			запустите программу и введите пароль `root` - пользователя  
		2. Терминал Linux - вызовите команду:
			
			> mysql -uroot -p

			и введите пароль `root` - пользователя

		3. Windows PowerShell - если `mysql` внесена в `PATH`, то аналогично п. 2.1.2 иначе, перейдите в  директорию установки СУБД, перейдите в папку `bin` и выполните команду:
			> .\mysql -uroot -p
	2. Создайте нового пользователя `lingo`, пароль можно указать произвольно (__замена логина недопустима__):
		> CREATE USER lingo IDENTIFIED BY 'password';
	3. Создайте новую базу данных:
		>CREATE DATABASE lingo;
		
		_Имя базы данных может быть изменено, однако, обязательно внесите изменения в настройки сервиса (см. `Установка` - п. 2.5)_
	4. Выдайте права новому пользователю:
		>GRANT ALL PRIVILEGES ON lingo.* TO lingo;
	5. Настройка параметров подключения
	 	
		1. Перейдите в директорию хранения исходного кода системы `pakt-work-tools`
		2. Текстовым редактором откройте файл `pakt-work-tools/settings.py`
		3. Перейдите к объявлению объекта `DATABASES`:
			```Python
			DATABASES = {
				'default': {
					'ENGINE': 'django.db.backends.mysql',
					'NAME': 'DATABASE_NAME',
					'USER': 'lingo',
					'PASSWORD': 'PASSWORD',
					'HOST': '127.0.0.1',
					'PORT': '3306',
					'CHARSET': 'utf8mb4',
				}
			}
			```
		4. Укажите название созданной базы данных вместо `DATABASE_NAME` (по умолчанию `lingo`)
		5. Укажите пароль созданного пользователя `lingo` вместо значения `PASSWORD`
		6. Если при установке СУБД вы изменяли какие-либо стандартные настройки, их также необходимо изменить и здесь. Описание настроек:
			- ENGINE - Встроенная сервернная база данных для использования(оставить как есть)
			- NAME - Имя используемой БД
			- USER - Имя пользователя
			- PASSWORD - Пароль пользователя
			- HOST - Хост, который используется при подключении к базе данных(по умолчанию: 127.0.0.1)
			- PORT - Порт, используемый при установке и настройки системы управления базами данных(по умолчанию: 3306)

	6. Создание миграций:
		1. Перейдите в корневую директорию сервиса
		2. Запустите скрипт
			> python create_migrations.py
		3. Если во время выполнения не было отображено ошибок или предупреждений введите __Y__  после того как скрипт запросит вашего решения. Иначе, проверьте корректность установки/подключения базы данных, а также убедитесь в том, что она не содержит каких-либо таблиц.

3. __Восстановление базы данных из дампа__
	
	* __Важно__: для успешного развертывания дампа с последующем подключением к системе, `.sql` файл самого дампа должен быть создан в соответствии с инструкцией `Дополнительно` - `Создание дампа для pakt-work-tools`. Также, при выполнении описанных ниже действий работа сервиса должна быть остановлена.
	1. Если ваша база данных пуста и в ней отсутсвуют таблицы (т.е. после успешного выполнения пункта 2), то выполните следующую команду (предварительно перейдя к директории хранения `mysql` если она не занесена в `PATH`, см.  п. 1.3):
		> mysql -ulingo -p lingo < PATH_TO_DUMP_FILE
	
		где `PATH_TO_DUMP_FILE` является путём к самому `.sql` файлу дампа.
		
		_Обратите внимание, что импорт данных из дампа требует наличия прав Администратора, в случае работы в WIndows OS, рекомендуется проводить данную операцию через командную строку (cmd) запущенную от имени администратора_
	2. Если ваша база данных `lingo` не пуста:
		1. Перейдите в консоль СУБД и выполните команды:
		 	> drop database lingo;
		 
		 	> create database lingo;
		
		2. Перейдите в корневую директорию сервиса и выполните скрипт:	
			> python drop_migrations.py
		3. Выполните все действия из `Установка` - п. 2.6.
		4. Выполните действия из первого пункта данного раздела.

4. __Запуск сервиса__
	
	 - После выполнения всех пунктов раздела установка, для запуска сервиса достаточно перейти в корневую директорию и запустить скрипт:

	 	> python manage.py runserver

	- __Важно__ все указанные скрипты необходимо выполнять в виртуальном окружении созданном в `Установка` - п. 1.

5. __Удаление сервиса__
	
	1. Перейдите в консоль управления СУБД с правами `root`-пользователя:
		
		1. Удалите базу данных:
			> drop database lingo;
		2. Удалите пользователя:
			> drop user lingo;
	3. Удалите папку содержащую проект и виртуальное окружение
	4. Удалите [MySQL](https://dev.mysql.com/doc/workbench/en/wb-windows-uninstalling.html)/[MariaDB](https://mariadb.com/kb/en/uninstall-or-delete-mariadb-completely-for-re-installation/)


## ***Дополнительно***
- Создание дампа для pakt-work-tools 
	```
	mysqldump -ulingo -p lingo --no-tablespaces --complete-insert --no-create-info --lock-tables=True --routines --ignore-table=lingo.auth_group --ignore-table=lingo.auth_group_permissions --ignore-table=lingo.auth_permission --ignore-table=lingo.django_admin_log --ignore-table=lingo.django_content_type --ignore-table=lingo.django_migrations --ignore-table=lingo.django_session  > dump.sql
	```

### Создание Python пакета
Библиотека (модуль аннотирования корпуса) содержит setup.py скрипт для создания python пакета.
Команда создания пакета:
```shell
python setup.py bdist_wheel --universal
```
После выполнения команды создается каталог dist с пакетом pakt_wor_tools-...-any.whl, который можно использовать для установки библиотеки.

### *Ошибка запуска вирт.окружения:*
CategoryInfo          : Ошибка безопасности: (:) [], PSSecurityException
FullyQualifiedErrorId : UnauthorizedAccess

Решение проблемы:
- Открываем терминал PowerShell от админа.
- Вставляем и запускаем - Set-ExecutionPolicy RemoteSigned
- На вопрос отвечаем - A

### Автоматическое тестирование кода библиотеки
Запуск тестов осуществляется средствами Django:
```shell
python3 manage.py test
```
Для сохранения тестовой базы данных можно воспользоваться ключем `--keepdb`.
Оценка покрытия выполняется с помощью утилиты coverage:
```shell
coverage run --source='.' manage.py test --keepdb
coverage html --omit="search_app/*"
```
