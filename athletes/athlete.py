#!/usr/bin/env python3

class Athlete:
    """Athlete domain class"""

    def __init__(self, i):
        if "id" in i:
            self.id = i["id"]
        self.name = i["name"]
        self.surname = i["surname"]
        self.born = i["born"]
        self.sex = i["sex"]
        if "club" in i:
            self.club = i["club"]
        self.start = None
        self.finish = None

    def toString(self):
        return "Athlete id: {0}, name: {1}, surname: {2}, born: {3}, sex: {4}, club: {5}".format(self.id if hasattr(self, "id") else "", self.name, self.surname, self.born, self.sex, self.club if hasattr(self, "club") else "")
        #return "{0}  {1} {2}, {3}, {4}".format(self.id if hasattr(self, "id") else "", self.name, self.surname, self.born, self.club if hasattr(self, "club") else "")
