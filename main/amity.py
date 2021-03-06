import sys
import fileinput
from random import random, shuffle
from models.employees import Staff, Fellow
from models.rooms import Office, LivingSpace


class Amity(object):

    def __init__(self):
        self.fellows_list = []
        self.staff_list = []
        self.room_list = {
            'office': [],
            'livingspace': []
        }
        self.allocated = {
            'office': [],
            'livingspace': []
        }
        self.unallocated = []
        self.office_index = -1
        self.livingspace_index = -1

    def pre_populate_rooms(self, room_list, room_type):
        """Prepopulates amity with offices and livingspaces"""
        for room_name in room_list:
            room = Office(room_name) \
                if room_type.lower() == 'office' else LivingSpace(room_name)
            self.room_list[room_type.lower()].append(room)

    def get_employee_details(self, inputfile):
        """Filter employee details from input.txt file"""
        for line in fileinput.input(inputfile):
            line = line.split()
            employee_name = " ".join(line[:2])
            employee_type = line[2]
            if employee_type == "FELLOW":
                wants_housing = line[-1]
                self.fellows_list.append(Fellow(employee_name, wants_housing))
            else:
                self.staff_list.append(Staff(employee_name))

    def get_office(self):
        """Returns available office"""
        if self.office_index > -1:
            office = self.room_list['office'][self.office_index]
        if self.office_index < 0 or not office.available_space():
            self.office_index += 1
            office = self.room_list['office'][self.office_index]
            self.allocated['office'].append(office)
        return office

    def get_livingspace(self):
        """Returns available living space"""
        if self.livingspace_index > -1:
            livingspace = self.room_list['livingspace'][self.livingspace_index]
        if self.livingspace_index < 0 or not livingspace.available_space():
            self.livingspace_index += 1
            livingspace = self.room_list['livingspace'][self.livingspace_index]
            self.allocated['livingspace'].append(livingspace)
        return livingspace

    def assign_officespace(self):
        """Assign office to employees randomly"""
        employees = self.fellows_list + self.staff_list
        shuffle(employees)
        for employee in employees:
            office = self.get_office()
            if office is not None:
                employee.allocate_office(office)
                office.add_occupant(employee)
            else:
                self.unallocated.append(employee)

    def assign_livingspace(self):
        """Assign livingspace to fellows that want housing"""
        fellows = self.fellows_list
        shuffle(fellows)
        for fellow in fellows:
            if fellow.wants_housing:
                livingspace = self.get_livingspace()
                if livingspace is not None:
                    fellow.allocate_livingspace(livingspace)
                    livingspace.add_roomie(fellow)
                else:
                    self.unallocated.append(fellow)

    def get_allocations_list(self):
        """Return a list of offices allocated"""
        return self.allocated

    def print_allocations(self):
        """Print a list of allocations"""
        for key, value in self.allocated.iteritems():
            for room_name in value:
                print "{0}" .format(room_name)
                print room_name.get_occupants()

    def get_unallocated(self):
        """Return a list of unallocated employees"""
        return self.unallocated

    def print_unallocated_employees(self):
        """Print a list of employees that did not get space"""
        for employee in self.unallocated:
            print employee.name
