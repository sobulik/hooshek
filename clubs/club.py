#!/usr/bin/env python3

class Club:
    """Club domain class"""

    def __init__(self, i):
        self.id = i["id"]
        self.name = ""
        if "name" in i:
            self.name = i["name"]
        self.isSokol = False
        if "isSokol" in i:
            self.isSokol = i["isSokol"]

    def toString(self):
        return "Club id: {0}, name: {1}, {2}a Sokol".format(self.id, self.name, "" if self.isSokol else "not ")
