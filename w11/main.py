import Employee


def print_help():
    print('---------- Menu ----------')
    print('1. Add a new employee')
    print('2. List all')
    print('0. Quit this program')


def add_a_new_employee():
    id = input('Please enter the employee ID: ')
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
    employees.add(employee)
    print('The entry has been added.')


def list_all():
    for e in employees:
        print(e)


def quit_the_program():
    exit(0)


choices = (
    quit_the_program,
    add_a_new_employee,
    list_all,
)
employees = set()

if __name__ == '__main__':
    while True:
        print_help()
        choice = int(input('Enter your choice: '))
        choices[choice]()
