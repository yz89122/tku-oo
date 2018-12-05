import pickle
from . import Employee

class EmployeeDBHandler:
    def __init__(self, local_db='Employee.dat'):
        self.local_db = local_db
        try:
            with open(self.local_db, 'rb') as d_data:
                self.m_data = pickle.load(d_data)
                if not isinstance(self.m_data, dict):
                    self.m_data = dict()
        except Exception:
            self.m_data = dict()

    def add_or_update(self, employee: Employee):
        self.m_data[employee.id] = employee
    
    def delete(self, id):
        self.m_data.pop(id, None)

    def get_by_id(self, id) -> Employee:
        return self.m_data.get(id)

    def list_all(self):
        return self.m_data.values()

    def exist(self, id):
        return id in self.m_data

    def save_to_disk(self):
        with open(self.local_db, 'wb+') as d_data:
            pickle.dump(self.m_data, d_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_to_disk()
