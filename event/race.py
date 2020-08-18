#!/usr/bin/env python3

from util import util

import datetime

class Race:
    """Race domain class"""

    def __init__(self, i):
        self.age_min = i["age_min"]
        self.age_max = i["age_max"]
        self.sex = i["sex"]
        self.name = i["name"]
        self.distance = i["distance"]
        if "start" in i:
            self.start = util.parseTime(i["start"])
        if "interval" in i:
            self.interval_athlete = datetime.timedelta(i["athlete"])
            self.interval_groupby = i["groupby"]
        self.athletes = None

    def toString(self):
        pass
