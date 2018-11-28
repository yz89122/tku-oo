class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

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

    def __str__(self):
        return 'Name: {name}, ID: {id}, Shift: {shift}, Rate: {rate}'.format(
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

    def __str__(self):
        return 'Name: {name}, ID: {id}, Salary: {salary}, Bonus: {bonus}'.format(
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
