from . import Employee
from . import EmployeeDBHandler


def kb_create_employee(db_handler: EmployeeDBHandler):
    id = input('Please enter the employee ID: ')
    if db_handler.exist(id) and \
            input('ID: {id} already exist, do you want to override?[y/N] '.format(id=id)) != 'y':
        return
    name = input('The employee\'s name: ')
    type_ = int(input('Type (1) Worker (2) Supervisor: '))
    if type_ == 1:
        shift = int(input('Shift (1) day (2) night: '))
        rate = int(input('Rate: '))
        employee = Employee.Worker(id, name, shift, rate)
    else:
        salary = int(input('Salary: '))
        bonus = int(input('Bonus: '))
        employee = Employee.Supervisor(id, name, salary, bonus)

    db_handler.add_or_update(employee)
    print('The entry has been added.')


def list_all(db_handler: EmployeeDBHandler):
    for e in db_handler.list_all():
        print(e)


def kb_look_up_employee(db_handler: EmployeeDBHandler):
    id = input('Please enter the employee_id: ')
    employee = db_handler.get_by_id(id)
    if employee is not None:
        print(employee)
    else:
        print('Loop up fail! No such employee!')


def kb_change_existing_employee(db_handler: EmployeeDBHandler):
    id = input('Please enter the employee ID: ')
    print('Current:', db_handler.get_by_id(id))
    name = input('The employee\'s name: ')
    type_ = int(input('Type (1) Worker (2) Supervisor: '))
    if type_ == 1:
        shift = int(input('Shift (1) day (2) night: '))
        rate = int(input('Rate: '))
        employee = Employee.Worker(id, name, shift, rate)
    else:
        salary = int(input('Salary: '))
        bonus = int(input('Bonus: '))
        employee = Employee.Supervisor(id, name, salary, bonus)

    db_handler.add_or_update(employee)
    print('Information updated.')


def kb_delete_employee(db_handler: EmployeeDBHandler):
    id = input('Please enter the employee_id: ')
    db_handler.delete(id)
