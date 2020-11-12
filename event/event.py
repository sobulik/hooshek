#!/usr/bin/env python3

from .race import Race

from util import util

import datetime

class Event:
    """Event domain class"""

    def __init__(self, i):
        self.name = i["name"]
        self.date = i["date"]
        self.encoding_print = "utf-8"
        if "encoding_print" in i and i["encoding_print"] is not None:
            self.encoding_print = i["encoding_print"]

        self.eff_year = self.date.year
        if self.date.month < 7:
            self.eff_year -= 1

        self.mass = True
        if "interval" in i:
            self.mass = False
            self.start = util.parseTime(i["interval"]["start"])
            self.interval_race = datetime.timedelta(seconds=i["interval"]["race"])
            self.interval_athlete = datetime.timedelta(seconds=i["interval"]["athlete"])
            self.interval_groupby = i["interval"]["groupby"]

        self.races = tuple(map(lambda x: Race(x), i["races"]))

    def toString(self):
        return "Event name: {0}, date: {1}, effective year: {2}, start: {3}, mass: {4}, interval_race: {5}".format(self.name, self.date, self.eff_year, self.start if hasattr(self, "start") else "", self.mass, self.interval_race if hasattr(self, "interval_race") else "")
