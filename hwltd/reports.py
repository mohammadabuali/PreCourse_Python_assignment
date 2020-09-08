from hwltd.organization import *

def get_num_employees(department:Group, depth:int):
    groups = [department]
    employees_dict = dict()
    for i in range(depth):
        new_group = []
        while groups:
            group = groups.pop()
            employees_dict[group.name] = group.get_workers_amount()
            new_group += group.sub_groups
        groups = new_group
    return employees_dict

def get_average_salary(group):
    workers = group.get_workers()
    return sum([worker.get_salary() for worker in workers]) / len(workers)

def get_relational_salary(worker):
    group = worker.team
    avg_salary = get_average_salary(group)
    return {teammate: teammate.get_salary()/avg_salary for teammate in group.get_workers() if teammate != worker}

