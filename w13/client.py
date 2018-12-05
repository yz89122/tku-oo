
from collections import defaultdict

from nio.client import RequestHandler
from nio.client import Connector
from employee import Employee

class KBClient:
    def __init__(self, server, port):
        self.__server = server
        self.__port = port
        self.__op = defaultdict(KBClient.not_a_choice, {
            '0': exit,
            '1': self.add_employee,
            '2': self.list_all,
            '3': self.lookup,
            '4': self.delete_employee
        })
        self.__handler = None

    @staticmethod
    def __help():
        print('''
        --------- Menu ---------
        1. Add a new employee
        2. List all
        3. Look up a employee
        # 4. Change an existing employee # XDD
        4. Delete a employee
        0. Quit the program
        ''')

    @staticmethod
    def not_a_choice():
        def p():
            print('not a choice')
        return p

    def add_employee(self):
        id = input('Please enter the employee ID: ')
        if self.__handler.check_existence(id) and \
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
            employee = Employee.Supervisor(name, id, salary, bonus)

        if self.__handler.add_employee(employee):
            print('The entry has been added.')
        else:
            print('unknown error')

    def list_all(self):
        for employee in self.__handler.list_all():
            print(Employee.make_employee(employee))

    def lookup(self):
        id = input('Please enter the employee_id: ')
        employee = self.__handler.get_by_id(id)
        if employee is not None:
            print(employee)
        else:
            print('Loop up fail! No such employee!')

    def delete_employee(self):
        id = input('Please enter the employee_id: ')
        if self.__handler.check_existence(id):
            self.__handler.delete_employee(id)
        else:
            print('Employee not exist')

    def start(self):
        with Connector(self.__server, self.__port) as c:
            self.__handler = RequestHandler(c)
            while True:
                KBClient.__help()
                self.__op[input('Enter your choice: ')]()

if __name__ == '__main__':
    client = KBClient('127.0.0.1', 20001)
    client.start()
