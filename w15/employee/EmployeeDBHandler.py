
import sqlite3
from threading import Lock

from . import Employee

class EmployeeDBHandler:
    def __init__(self, local_db='Employee.db'):
        self.local_db = local_db
        self.__db = None
        self.__execution_lock = Lock()

    def add_or_update(self, employee: Employee):
        self.__add_employee_type(employee.type)
        self.__query_write('''
INSERT OR REPLACE INTO `employees`
VALUES
(
    (
        SELECT `id` FROM `employees`
        WHERE `employee_id` = :employee_id
    ),
    :employee_id ,
    (
        SELECT `id` FROM `employee_types`
        WHERE `type` = :type
    ),
    :name ,
    :salary_or_shift ,
    :bonus_or_rate
);''',
            {
                'employee_id': employee.id,
                'type': employee.type,
                'name': employee.name,
                'salary_or_shift': employee.salary if employee.type == 'supervisor' else employee.shift,
                'bonus_or_rate': employee.bonus if employee.type == 'supervisor' else employee.rate
            })
    
    def delete(self, id):
        self.__query_write('''
DELETE FROM `employees` WHERE `employee_id` = :employee_id ;''',
            {'employee_id': id})

    def get_by_id(self, id) -> Employee:
        query_result = self.__query_read('''
SELECT * FROM `employees`
WHERE `employee_id` = :employee_id ;''',
            {'employee_id': id})
        try:
            row = query_result[0]
            employee_type = row[2]
            employee_class = Employee.Worker
            if employee_type == 'supervisor':
                employee_class = Employee.Supervisor
            return employee_class(
                row[1],
                row[3],
                row[4],
                row[5]
            )
        except IndexError:
            return None

    def list_all(self):
        result = list()
        query_result = self.__query_read('''SELECT * FROM `employees`;''')
        for row in query_result:
            employee_type = row[2]
            employee_class = Employee.Worker
            if employee_type == 'supervisor':
                employee_class = Employee.Supervisor
            result.append(employee_class(
                row[1],
                row[3],
                row[4],
                row[5]
            ))
        return result

    def exist(self, id):
        return self.get_by_id(id) is not None

    def commit(self):
        with self.__execution_lock:
            self.__db.commit()

    def __query_read(self, query, *args, **kwargs):
        with self.__execution_lock:
            return self.__db.execute(query, *args, **kwargs).fetchall()

    def __query_write(self, query, *args, **kwargs):
        with self.__execution_lock:
            self.__db.execute(query, *args, **kwargs)

    def __add_employee_type(self, employee_type):
        self.__query_write('''
INSERT OR REPLACE INTO `employee_types`
VALUES
(
    (
        SELECT `id` FROM `employee_types`
        WHERE `type` = :type
    ),
    :type
);''', {'type': employee_type})

    def __create_tables(self):
        self.__db.execute('''
CREATE TABLE IF NOT EXISTS `employee_types`
(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `type` TEXT UNIQUE NOT NULL
);''')
        self.__db.execute('''
CREATE UNIQUE INDEX IF NOT EXISTS
`index_employee_types_id` ON `employee_types`(`id`);''')
        self.__db.execute('''
CREATE UNIQUE INDEX IF NOT EXISTS
`index_employee_types_type` ON `employee_types`(`type`);''')

        self.__db.execute('''
CREATE TABLE IF NOT EXISTS `employees`
(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `employee_id` TEXT UNIQUE NOT NULL,
    `type` INTEGER NOT NULL,
    `name` TEXT,
    `salary_or_shift` INTEGER,
    `bonus_or_rate` INTEGER
);''')
        self.__db.execute('''
CREATE UNIQUE INDEX IF NOT EXISTS
`index_employees_id` ON `employees`(`id`);''')
        self.__db.execute('''
CREATE UNIQUE INDEX IF NOT EXISTS
`index_employees_employee_id` ON `employees`(`employee_id`);''')

    def __enter__(self):
        self.__db = sqlite3.connect(self.local_db, check_same_thread=False)
        self.__create_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()
        self.__db.close()
