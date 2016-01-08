from employees import Staff, Fellow


class Room(object):
    def __init__(self, room_name):
        self.room_name = room_name
        self.occupants = []

    def get_occupants(self):
        """Gives the list of current occupiers of a room"""
        return self.occupants

    def current_number(self):
        """checks for current occupancy of a room"""
        return len(self.occupants)

    def available_space(self):
        """Checks if room is at maximum capacity"""
        """returns true if space is available"""
        if self.current_number() < self.maximum_members:
            return True
        else:
            return False

   


class Office(Room):
    maximum_members = 6
    room_type = "Office"

    def add_occupant(self, employee):
        "adds an employees name to list of office occupants"
        if self.available_space() is True:
            if isinstance(employee, Staff) or isinstance(employee, Fellow):
                self.occupants.append(employee)
                with open('office_allocation.txt', 'a') as f:
                    f.write(employee.name + " " + self.room_name + "\n")
            return self.occupants

    def __repr__(self):
        return "{0} (Office)".format(self.room_name)        


class LivingSpace(Room):
    maximum_members = 4
    room_type = "LivingSpace"

    def add_occupant(self, fellow):
        """add fellows name to list of livingspace occupants"""
        if self.available_space() is True:
            self.occupants.append(fellow)
            with open('rooms_allocated.txt', 'a') as f:
                f.write(fellow.name + " " + self.room_name + "\n")
        return self.occupants