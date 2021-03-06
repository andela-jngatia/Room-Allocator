import unittest
import nose
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from main.amity import Amity
from models.employees import Staff, Fellow
from models.rooms import Office, LivingSpace

living_space_names = ['Brown', 'Cyan', 'Turquiose', 'White',
                      'Orange', 'Ruby', 'Lilac', 'Sapphire',
                      'Emerald', 'Quartz']
office_names = ['Hogwarts', 'Valhalla', 'Roundtable', 'Quahog',
                'Springfield', 'Krypton', 'Oculus', 'Narnia',
                'Gotham', 'Nowhere']

file_input = 'data/sample.txt'


class TestModels(unittest.TestCase):
    """Test models created"""
    def setUp(self):
        self.amity = Amity()
        self.office = Office('Krypton')
        self.livingspace = LivingSpace('Sapphire')
        self.fellow = Fellow('Joan Ngatia', True)
        self.staff = Staff('Anthony Nandaa')
        self.amity.get_employee_details(file_input)

    def test_office_creation(self):
        """Test correct office instantiation"""
        self.assertIsInstance(self.office, Office)

    def test_livingspace_creation(self):
        """Test correct livingspace instatiation"""
        self.assertIsInstance(self.livingspace, LivingSpace)

    def test_employee_type(self):
        """Test correct assignment of employee type"""
        self.assertIsInstance(self.fellow, Fellow)
        self.assertIsInstance(self.staff, Staff)

    def test_return_current_occupants(self):
        """Test return correct number of room occupants"""
        self.office.add_occupant(self.fellow)
        self.office.add_occupant(self.staff)
        self.livingspace.add_roomie(self.fellow)
        self.assertEquals(self.office.current_number(), 2)
        self.assertEquals(self.livingspace.current_number(), 1)
        self.assertTrue(self.office.available_space())
        self.assertTrue(self.livingspace.available_space())


class TestRoomAllocation(unittest.TestCase):
    """Test main allocation system"""
    def setUp(self):
        self.amity = Amity()
        self.amity.pre_populate_rooms(living_space_names, 'livingspace')
        self.amity.pre_populate_rooms(office_names, 'office')
        self.amity.get_employee_details(file_input)

    def test_amity_prepopulation(self):
        """Test correct prepolation of Amity"""
        self.assertEquals(len(self.amity.room_list['livingspace']), 10)
        self.assertEquals(len(self.amity.room_list['office']), 10)

    def test_allocations_list(self):
        """Test getting allocations list as per sample file input"""
        self.amity.assign_officespace()
        self.amity.assign_livingspace()
        allocations = self.amity.get_allocations_list()
        self.assertIsNotNone(allocations)
        self.assertEqual(len(allocations['office']), 7)
        self.assertEqual(len(allocations['livingspace']), 4)

        # Store employee instances for testing"""
        self.staff = Staff("NYAMBURA KIHORO")
        self.fellow1 = Fellow("ALEX MWALEH", True)
        self.fellow2 = Fellow("PAULIO NGATIA")

        # Test correct allocation to rooms"""
        livingspaces_occupied = allocations['livingspace']
        occupants = []
        for room in livingspaces_occupied:
            occupants += room.get_occupants()
        self.assertTrue(self.fellow1 in occupants)
        self.assertFalse(self.staff in occupants)
        self.assertFalse(self.fellow2 in occupants)

    def test_unallocated_list(self):
        """Tests getting list of unallocated employees"""
        self.amity.assign_officespace()
        self.amity.assign_livingspace()
        unallocated = self.amity.get_unallocated()
        self.assertEqual(len(unallocated), 0)


if __name__ == '__main__':
    nose.run()
