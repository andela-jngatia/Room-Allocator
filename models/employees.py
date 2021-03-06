class Employee(object):
    """Represents employees at amity"""
    def __init__(self, name):
        self.name = name
        self.office = None

    def allocate_office(self, office):
        """Assign office to employee"""
        self.office = office
        return self.office

    def has_office(self):
        return True if self.office is not None else False

    def __repr__(self):
        return "{0}".format(self.name)

    def __eq__(self, obj):
        return self.name == obj.name and self.__class__ == obj.__class__


class Fellow(Employee):
    """Fellow inherits from Employee class
       fellow has choice of housing within Amity"""
    def __init__(self, name, wants_housing='N'):
        self.name = name
        self.livingspace = None
        self.wants_housing = True if wants_housing == 'Y' else False

    def allocate_livingspace(self, room):
        """Assign living space to fellows"""
        self.livingspace = room
        return self.livingspace


class Staff(Employee):
    """Staff inherits from the Employee class"""
    pass
