from employee import EmployeeDBHandler
from employee import EmployeeFromKB


def print_help():
    print('''
    --------- Menu ---------
    1. Add a new employee
    2. List all
    3. Look up a employee
    4. Change an existing employee
    5. Delete a employee
    0. Quit the program
    ''')


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
