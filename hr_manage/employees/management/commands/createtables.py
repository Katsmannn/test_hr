# Проверяет, существуют ли в базе данных таблицы positions и employees.
# Если таблицы отсутствуют, то они создаются в базе данных.

from django.core.management.base import BaseCommand
import psycopg2 as pg2
from dotenv import dotenv_values
from django.conf import settings


# Получение параметров подключения к базе данных из файла .env
config = dotenv_values(str(settings.BASE_DIR.parent) + '/DATA/.env')
DB_NAME = config.get('DB_NAME')
DB_USER = config.get('DB_USER')
DB_PASSWORD = config.get('DB_PASSWORD')
DB_HOST = config.get('DB_HOST')


def table_is_exist(table_name):
    '''Проверяет, существует ли таблица table_name в базе данных.'''

    check_table_query = (
        'SELECT EXISTS'
        + '(SELECT * FROM information_schema.tables WHERE table_name=%s)'
    )

    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                       password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(check_table_query, (table_name,))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result


def create_table(query):
    '''Создаёт новую таблицу в базе данных запросом query.'''

    try:
        conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                           password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as ex:
        print(f'ОШИБКА! {ex}')


class Command(BaseCommand):
    help = 'Create tables EMPLOYEES and POSITIONS in database HR_DB'

    def handle(self, *args, **options):

        create_table_positions_query = (
            'CREATE TABLE positions '
            + '(id SERIAL PRIMARY KEY, name TEXT, category TEXT, '
            + 'UNIQUE (name, category))'
        )
        create_table_employees_query = (
            'CREATE TABLE employees '
            + '(id SERIAL PRIMARY KEY, full_name TEXT, birthday DATE, '
            + 'sex TEXT, '
            + 'position_id INT REFERENCES positions(id) ON DELETE RESTRICT, '
            + 'UNIQUE (full_name, birthday))'
        )
        create_tables_query = {
            'positions': create_table_positions_query,
            'employees': create_table_employees_query
        }

        for table_name, query in create_tables_query.items():
            if not table_is_exist(table_name):
                create_table(query)
                if table_is_exist(table_name):
                    print(f'Таблица {table_name} создана.')
                else:
                    print(
                        f'ВНИМАНИЕ! Не удалось создать таблицу {table_name}.'
                    )
            else:
                print(f'Таблица {table_name} существует.')
