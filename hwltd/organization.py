from workers.structure import *
import sys
import traceback
class Employees:
    def __init__(self, dict_employees):
        self.dict_employees = dict_employees

    def add_employee(self, name, email):
        self.dict_employees[email] = name

class HelloWorld:

    def __init__(self, path):
        self.departments = ['Engineering', 'HR', 'Finance']
        self.engineering_subgroups = ['SW', 'HW', 'CTO', 'System']
        self.HR_subgroups = ['Recruitment', 'Culture']
        self.finance_subgroups = ['Salaries', 'Budget']
        self.teams = ['infrastructure', 'app', 'drivers',
                      'qa', 'chip', 'board', 'power',
                      'design', 'poc', 'tech', 'staff',
                      'income', 'outcome',' cto', 'culture',
                      'salaries']
        self.all_groups = dict()
        self.allEmployees = Employees(dict())
        self.create_groups()
        self.create_employees(path)


    def create_groups(self):
        self.create_engineering_groups()
        self.create_finance_groups()
        self.create_hr_groups()

    def create_finance_groups(self):
        self.all_groups['Finance'] = Group('Finance', 'Finance')
        self.all_groups['Budget'] = Group('Budget', 'Budget',
                                               parent_group=self.all_groups['Finance'])
        self.all_groups['Salaries'] = Group('Salaries', 'Salaries',
                                           parent_group=self.all_groups['Finance'])
        self.all_groups['income'] = Group('income', 'income', parent_group=self.all_groups['Budget'])
        self.all_groups['outcome'] = Group('outcome', 'outcome', parent_group=self.all_groups['Budget'])
        self.all_groups['Finance'].sub_groups = [self.all_groups['Budget'], self.all_groups['Salaries']]
        self.all_groups['Budget'].sub_groups = [self.all_groups['income'], self.all_groups['outcome']]


    def create_hr_groups(self):
        self.all_groups['HR'] = Group('HR', 'HR')
        self.all_groups['Recruitment'] = Group('Recruitment','Recruitment',
                                               parent_group=self.all_groups['HR'])
        self.all_groups['Culture'] = Group('Culture', 'Culture',
                                               parent_group=self.all_groups['HR'])
        self.all_groups['tech'] = Group('tech', 'tech', parent_group=self.all_groups['Recruitment'])
        self.all_groups['staff'] = Group('staff', 'staff', parent_group=self.all_groups['Recruitment'])
        self.all_groups['HR'].sub_groups = [self.all_groups['Recruitment'], self.all_groups['Culture']]
        self.all_groups['Recruitment'].sub_groups = [self.all_groups['tech'], self.all_groups['staff']]


    def create_engineering_groups(self):
        teams = ['infrastructure', 'app', 'drivers',
                      'qa', 'chip', 'board', 'power',
                      'design', 'poc']
        self.all_groups['Engineering'] = Group('Engineering', 'Engineering department',)
        for team in self.engineering_subgroups:
            self.all_groups[team] = Group(team, team, parent_group=self.all_groups['Engineering'])

        for i, team in enumerate(teams):
            group = Group(team, team)
            if i < 4:
                group.parent_group = self.all_groups['SW']
            elif i < 7:
                group.parent_group = self.all_groups['HW']
            else:
                group.parent_group = self.all_groups['System']
            self.all_groups[team] = group
        self.all_groups['Engineering'].sub_groups = [self.all_groups[team] for team in self.engineering_subgroups]
        self.all_groups['SW'].sub_groups = [self.all_groups[team] for team in teams[:4]]
        self.all_groups['HW'].sub_groups = [self.all_groups[team] for team in teams[4:7]]
        self.all_groups['System'].sub_groups = [self.all_groups[team] for team in teams[7:]]


    def create_employees(self,path):
        data = self.readFile(path)
        for employee_data in data:
            employee_dict = self.build_dict_employees(employee_data)
            try:
                self.fix_employee(employee_dict)
                self.create_a_single_employee(employee_dict)

            except:
                traceback.print_tb(sys.exc_info()[2])
                continue

    def create_a_single_employee(self, data):
        last_name = data['last_name']
        first_name = data['first_name']
        year_of_birth = data['year_of_birth']
        email = data['email']
        team = data['team']
        phones = [Phone(phone) for phone in data['phones']]
        addressLst = data['address']
        if len(addressLst) == 3:
            address = PobAddress(addressLst[0], addressLst[1], addressLst[2])
        else:
            address = StreetAddress(addressLst[0], addressLst[1], addressLst[2], addressLst[3])
        role = data['role']
        if role.lower() == 'staff':
            salary = data['data'][0]
            employee = Worker(last_name, first_name, year_of_birth,
                              email, phones, address, team, salary)

        elif role.lower() == 'engineer':
            salary = data['data'][0]
            bonus = data['data'][1]
            employee = Engineer(last_name,first_name, year_of_birth,
                                email,phones,address,team,salary, bonus)
        else:
            salary = data['data'][0]
            commision = data['data'][1]
            deals = data['data'][2:]
            employee = SalesPerson(last_name, first_name, year_of_birth,
                                email, phones, address, team, salary, commision,
                                deals)
        t = self.all_groups[team]
        t.add_worker(employee)
        self.allEmployees.add_employee(first_name + " " + last_name, email)
        return employee

    def readFile(self, path):
        with open(path, 'r') as file:
            return [line.strip('#') for line in file.readlines()]
    def build_dict_employees(self, data):
        data = data.split(',')
        data = [d.strip(' ') for d in data]
        lst_employees = ['last_name', 'first_name', 'year_of_birth',
                         'email', 'phones', 'address', 'team',
                         'role', 'data']
        employee_dict = {lst_employees[i]: d for i,d in enumerate(data)}
        return employee_dict

    def fix_employee(self, employee_dict):
        phones = employee_dict['phones']
        phones = phones.split(';')
        employee_dict['phones'] = phones
        address = employee_dict['address']
        address = address.split(';')
        assert len(address) == 3 or len(address) == 4, "wrong address format"
        employee_dict['address'] = address
        team = employee_dict['team']
        assert team.lower() in self.teams, "team not found"
        role = employee_dict['role']
        data = employee_dict['data']
        assert role.lower() in ['staff', 'engineer', 'sales'], "role not found"
        regex = '^[0-9]+([.][0-9]+)?$'
        data = data.split(';')
        if role == 'staff':
            assert len(data) == 1 and re.search(regex, data[0]), "payment data error"
        if role == 'engineer':
            assert len(data) == 2 and re.search(regex, data[0]) \
                                  and re.search(regex, data[1]), "payment data error"
        if role == 'sales':
            assert len(data) >= 2, "payment data error"
            for i in data:
                assert re.search(regex, i), "payment data error"
        employee_dict['data'] = data



