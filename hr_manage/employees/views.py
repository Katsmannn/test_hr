import datetime as dt

from django.shortcuts import render, redirect
import psycopg2 as pg2
from dotenv import dotenv_values
from django.conf import settings
from django.core.paginator import Paginator

from .forms import PositionForm, EmployeeForm


# Получение параметров подключения к базе данных из файла .env
config = dotenv_values(str(settings.BASE_DIR.parent) + '/DATA/.env')
DB_NAME = config.get('DB_NAME')
DB_USER = config.get('DB_USER')
DB_PASSWORD = config.get('DB_PASSWORD')
DB_HOST = config.get('DB_HOST')
PER_PAGE = config.get('PER_PAGE')


def index(request):
    pass


def positions(request):
    all_positions_query = 'SELECT * FROM positions ORDER BY name'

    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(all_positions_query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(result, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'positions.html', {'page': page})


def new_position(request):
    form = PositionForm(request.POST or None)
    if form.is_valid():
        new_position_name = form.cleaned_data['name']
        new_position_category = form.cleaned_data['category']

        create_position_query = f'INSERT INTO positions (name, category) VALUES (%s, %s)'
        conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute(create_position_query, (new_position_name, new_position_category))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('positions')
    return render(request, 'newposition.html', {'form': form})


def edit_position(request, position_id):
    get_position_query = 'SELECT * FROM positions WHERE id=%s'
    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(get_position_query, (position_id,))
    position = cur.fetchone()
    position_name = position[1]
    position_category = position[2]
    form = PositionForm(request.POST or None, initial={'name': position_name, 'category': position_category})
    if form.is_valid():
        new_position_name = form.cleaned_data['name']
        new_position_category = form.cleaned_data['category']
        update_position_query = "UPDATE positions SET name=%s category=%s WHERE id=%s;"

        cur.execute(update_position_query, (new_position_name, new_position_category, position_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('positions')
    return render(request, 'editposition.html', {'form': form, 'position_id': position_id})


def employees(request):
    all_employees_query = 'SELECT employees.id, employees.full_name, positions.name FROM employees JOIN positions ON employees.position_id=positions.id ORDER BY employees.full_name'

    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(all_employees_query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    paginator = Paginator(result, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'employees.html', {'page': page})


def new_employee(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        new_employee_name = form.cleaned_data['name']
        new_employee_position = form.cleaned_data['position']
        new_employee_birthday = form.cleaned_data['birthday']
        new_employee_sex = form.cleaned_data['sex']

        create_employee_query = f'INSERT INTO employees (full_name, position_id, birthday, sex) VALUES (%s, %s, %s, %s)'
        conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute(create_employee_query, (new_employee_name, new_employee_position, new_employee_birthday, new_employee_sex))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('employees')
    return render(request, 'newemployee.html', {'form': form})


def edit_employee(request, employee_id):
    get_employee_query = 'SELECT * FROM employees WHERE id=%s'
    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(get_employee_query, (employee_id,))
    employee = cur.fetchone()
    employee_name = employee[1]
    employee_birthday = dt.datetime.strftime(employee[2], '%d.%m.%Y')
    employee_sex = employee[3]
    employee_position = employee[4]
    form = EmployeeForm(request.POST or None, initial={'name': employee_name, 'birthday': employee_birthday, 'sex': employee_sex, 'position': employee_position})
    if form.is_valid():
        new_employee_name = form.cleaned_data['name']
        new_employee_birthday = form.cleaned_data['birthday']
        new_employee_sex = form.cleaned_data['sex']
        new_employee_position = form.cleaned_data['position']
        update_employees_query = "UPDATE employees SET full_name=%s, birthday=%s, sex=%s, position_id=%s WHERE id=%s;"
        pg_query = cur.execute(update_employees_query, (new_employee_name, new_employee_birthday, employee_sex, new_employee_position, employee_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('employee_detail', employee_id=employee_id)
    return render(request, 'editemployee.html', {'form': form, 'employee_id': employee_id})


def employee_detail(request, employee_id):
    get_employee_query = 'SELECT employees.id, employees.full_name, employees.birthday, employees.sex, positions.name, positions.category FROM employees INNER JOIN positions on employees.position_id=positions.id WHERE employees.id=%s'

    conn = pg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(get_employee_query, (employee_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    employee = (
        result[0],
        result[1],
        result[3],
        (dt.date.today() - result[2]).days // 365,
        result[4] + '/' + result[5],
    )
        
        
    return render(request, 'employeedetail.html', {'employee': employee})

