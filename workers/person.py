import re
class Person:
    id = 1

    @classmethod
    def idIncrease(cls):
        cls.id += 1

    @classmethod
    def checkRegex(cls, email):
        regex =  '^[a-zA-Z0-9_]+[@]([a-z]+[.])+hwltd.com$'
        if re.search(regex, email):
            return True
        return False

    def __init__(self, lastName, firstName,
                 email, year_of_birth=None, phones=[], address=None):
        self.name = firstName + ' ' + lastName,
        self.lastName = lastName,
        self.year_of_birth = year_of_birth
        self.id = Person.id,
        Person.idIncrease()
        assert Person.checkRegex(email), "email format is wrong"
        self.email = email,
        self.phones = phones
        self.address = address
        assert firstName and lastName and email


class Phone:
    @classmethod
    def checkNumber(cls, number):
        regex = '^[+]?([0-9]*-?)+$'
        if re.search(regex, number):
            return True
        return False
    def __init__(self, number):
        assert number
        if not Phone.checkNumber(number):
            raise ValueError
        self.number = number


class Address:
    def __init__(self, country, city):
        assert country and city
        self.country = country
        self.city = city

    def _additionalInfo(self):
        raise NotImplementedError("I need to be implemented")

    def formattedAddress(self):
        try:
            pretty_string = "My country is: " + self.country +\
                            ", and my city is: " + self.city + \
                             self._additionalInfo()
        except:
            pretty_string = "My country is: " + self.country +\
                            ", and my city is: " + self.city
        finally:
            return pretty_string


class StreetAddress(Address):
    def __init__(self, country, city, streetName, houseNumber):
        super().__init__(country, city)
        self.streetName = streetName
        self.houseNumber = houseNumber


    def _additionalInfo(self):
        return ", I live in street: " + self.streetName +\
                ", and my house number is: " + self.houseNumber

class PobAddress(Address):
    def __init__(self, country, city, pob):
        super().__init__(country, city)
        self.pob = pob

    def _additionalInfo(self):
        return ", and you can send me mail at " + self.pob
