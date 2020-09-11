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
        if "eval" in i:
            self.eval = list()
            for e in i["eval"]:
                evaluation = dict()
                evaluation["age_min"] = e["age_min"]
                evaluation["age_max"] = e["age_max"]
                self.eval.append(evaluation)
        if "start" in i:
            self.start = util.parseTime(i["start"])
        if "interval" in i:
            self.interval_athlete = datetime.timedelta(i["athlete"])
            self.interval_groupby = i["groupby"]
        self.athletes = None

    def toString(self):
        pass
