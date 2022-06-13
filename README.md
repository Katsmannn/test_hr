# HR-менеджер
Система управления личными карточками сотрудников
## Функционал
Система позволяет вести учёт персонала. Личные карточки содержат информацию о сотруднике: ФИО, дата рождения (возраст), должность, пол.  
Есть возможность создания, редактирования, удаления карточки сотрудника, а также создавать, изменять и удалять должности, доступные для выбора в карточке сотрудника.
## Используемые технологии
UBUNTU, PostgreSQL, PYTHON, DJANGO, BOOTSTRAP
## Развёртывание системы
Перед развёртыванием системы необходимо установить PostgreSQL и создать в нем базу данных.
1. Склонировать репозиторий:
```
$ git clone git@github.com:Katsmannn/test_hr.git
```
2. Зайти в каталог проекта
```
$ cd test_hr/
```
3. Создать каталог DATA:
```
$ mkdir DATA
```
4. В каталоге DATA создать файл с параметрами:
```
$ nano DATA/.env
```
Файл должен содержать параметры:
```
DB_NAME = # имя базы данных
DB_HOST = # хост базы данных
DB_USER = # пользователь PostgreSQL
DB_PASSWORD = # пароль PostgreSQL

PER_PAGE=6 # количество записей на странице для пагинатора

```
5. Создать и запустить виртуальное окружение, установить зависимости:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
6. Создать в базе данных необходимые для работы системы таблицы:
```
$ python3 hr_manage/manage.py createtables
```
7. Запустить сервер отладки Django:
```
$ python3 hr_manage/manage.py runserver
```
Система доступна по адресам:  
-- список должностей
```
127.0.0.1:8000/positions
```
-- список сотрудников 
```
127.0.0.1:8000/employees
```
## Таблицы базы данных
Таблицы базы данных создаются запросами:
```
-- Таблица должностей
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    name TEXT,
    category TEXT,
    UNIQUE (name, category)
);

-- Таблица сотрудников
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    birthday DATE,
    sex TEXT,
    position_id INT REFERENCES positions(id) ON DELETE RESTRICT,
    UNIQUE (full_name, birthday)
);
```
![](https://img.shields.io/github/languages/count/katsmannn/test_hr)