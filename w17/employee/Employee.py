def make_employee(d: dict):
    if {'id', 'name', 'type'} < d.keys():
        if d['type'] == 'worker':
            if {'shift', 'rate'} < d.keys():
                return Worker(
                    d['id'],
                    d['name'],
                    d['shift'],
                    d['rate']
                )
        else:
            if {'bonus', 'salary'} < d.keys():
                return Supervisor(
                    d['name'],
                    d['id'],
                    d['salary'],
                    d['bonus']
                )


class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def to_dict(self):
        return dict({
            'type': 'employee',
            'name': self.name,
            'id': self.id
        })

    def __str__(self):
        return 'Name: {name}, ID {id}'.format(
            name=self.name,
            id=self.id
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (type(other) == Employee and self.id == other.id) or other == self.id

    def __hash__(self):
        return hash(self.id)


class Worker(Employee):
    def __init__(self, id, name, shift, rate):
        Employee.__init__(self, name, id)
        self.shift = shift
        self.rate = rate
        self.type = 'worker'

    def to_dict(self):
        return dict({
            'type': self.type,
            'id': self.id,
            'name': self.name,
            'shift': self.shift,
            'rate': self.rate
        })

    def __str__(self):
        return 'W- Name: {name},\tID: {id},\tShift: {shift},\tRate: {rate}'.format(
            name=self.name,
            id=self.id,
            shift=self.shift,
            rate=self.rate
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (type(other) == Worker and self.id == other.id) or other == self.id

    def __hash__(self):
        return hash(self.id)


class Supervisor(Employee):
    def __init__(self, name, id, salary, bonus):
        Employee.__init__(self, name, id)
        self.salary = salary
        self.bonus = bonus
        self.type = 'supervisor'

    def to_dict(self):
        return dict({
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'salary': self.salary,
            'bonus': self.bonus
        })

    def __str__(self):
        return 'S- Name: {name},\tID: {id},\tSalary: {salary},\tBonus: {bonus}'.format(
            name=self.name,
            id=self.id,
            salary=self.salary,
            bonus=self.bonus
        )
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (type(other) == Supervisor and self.id == other.id) or other == self.id

    def __hash__(self):
        return hash(self.id)
