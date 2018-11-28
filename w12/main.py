from employee import EmployeeDBHandler
from employee import EmployeeFromKB


def print_help():
    print('---------- Menu ----------')
    print('1. Add a new employee')
    print('2. List all')
    print('3. Look up a employee')
    print('4. Change an existing employee')
    print('5. Delete a employee')
    print('0. Quit this program')


def quit_this_program(*arg):
    exit(0)


if __name__ == '__main__':
    choices = (
        quit_this_program,
        EmployeeFromKB.kb_create_employee,
        EmployeeFromKB.list_all,
        EmployeeFromKB.kb_look_up_employee,
        EmployeeFromKB.kb_change_existing_employee,
        EmployeeFromKB.kb_delete_employee
    )

    with EmployeeDBHandler.EmployeeDBHandler() as db_handler:
        while True:
            print_help()
            choice = int(input('Enter your choice: '))
            choices[choice](db_handler)
