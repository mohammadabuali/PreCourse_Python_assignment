from workers.person import *
class Group:
    def __init__(self, name, description, parent_group=None,
                 sub_groups=None, workers=None):
        self.name = name
        self.description = description
        self.parent_group = parent_group
        self.sub_groups = sub_groups if sub_groups is not None else []
        self.workers = workers if workers is not None else []
        assert not sub_groups or not workers

    def get_parents(self):
        current = self
        while current.parent_group is not None:
            yield current.parent_group
            current = current.parent_group

    def get_workers(self):
        if self.workers:
            return (i for i in self.workers)
        return (j for i in self.sub_groups for j in i.get_workers())
    def get_workers_amount(self):
        if self.workers:
            return len(self.workers)
        sum = 0
        for group in self.sub_groups:
            sum += group.get_workers_amount()
        return sum


    def add_worker(self, worker):
        self.workers.append(worker)

class Worker:
    def __init__(self, last_name, first_name,
                 year_of_bearth, email, phones,
                 address, team, salary):
        self.team = team
        self.person = Person(last_name, first_name, email=email,
                        year_of_birth=year_of_bearth, phones=phones, address=address)
        self.salary = salary

    def get_salary(self):
        return self.salary




class Engineer(Worker):
    def __init__(self,last_name, first_name,
                 year_of_bearth, email, phones,
                 address, team, salary, bonus):
        super().__init__(last_name, first_name,
                 year_of_bearth, email, phones,
                 address, team, salary)
        self.bonus = bonus


    def get_salary(self):
        return self.salary + self.bonus

class SalesPerson(Worker):
    def __init__(self,last_name, first_name,
                 year_of_bearth, email, phones,
                 address, team, salary, commision, deals):
        super().__init__(last_name, first_name,
                 year_of_bearth, email, phones,
                 address, team, salary)
        self.commision = commision
        self.deals = deals

    def get_salary(self):
        return self.salary + self.commision * sum(self.deals)
