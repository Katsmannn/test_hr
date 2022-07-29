from django import forms
from django.conf import settings
import psycopg2 as pg2
from dotenv import dotenv_values


# Получение параметров подключения к базе данных из файла .env
config = dotenv_values(str(settings.BASE_DIR.parent) + '/DATA/.env')
DB_NAME = config.get('DB_NAME')
DB_USER = config.get('DB_USER')
DB_PASSWORD = config.get('DB_PASSWORD')
DB_HOST = config.get('DB_HOST')


# Список выбора значений для поля "категория"
CATEGORY_CHOICE = [
    ('рабочий', 'рабочий'),
    ('служащий', 'служащий'),
    ('специалист', 'специалист'),
]
# Список выбора значений для поля "пол"
SEX_CHOICE = [
    ('муж.', 'муж.'),
    ('жен.', 'жен.'),
]


def _get_positions():
    '''
    Получение списка должностей для выбора в поле "должность".
    '''

    all_positions_query = 'SELECT id, name, category FROM positions'

    with pg2.connect(
        dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(all_positions_query)
            result = cur.fetchall()
    return [(x[0], x[1] + '/' + x[2]) for x in result]


class PositionForm(forms.Form):
    '''
    Форма для заполнения полей должностей.
    '''

    # название должности
    name = forms.CharField(label='Должность', max_length=100)
    # категория должности
    category = forms.ChoiceField(label='Категория', choices=CATEGORY_CHOICE)


class EmployeeForm(forms.Form):
    '''
    Форма для заполнения полей сотрудника.
    '''

    # название сотрудника
    name = forms.CharField(label='ФИО', max_length=100)
    # пол сотрудника
    sex = forms.ChoiceField(label='Пол', choices=SEX_CHOICE)
    # дата рождения сотрудника
    birthday = forms.DateField(label='Дата рождения',
                               input_formats=['%d.%m.%Y'])
    # должность сотрудника (id из таблицы должностей)
    position = forms.ChoiceField(label='Должность/категория', choices=[],
                                 required=False)

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['position'].choices = _get_positions()

