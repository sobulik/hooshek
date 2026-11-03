#!/usr/bin/env python3

import datetime

import hooshek.event.race
import hooshek.util.util


class Event:
    """Event domain class"""

    def __init__(self, i):
        self.version = i["version"]
        self.name = i["name"]
        self.date = i["date"]
        self.encoding_print = "utf-8"
        try:
            self.location = i["location"]
        except KeyError:
            pass
        try:
            self.organizer = i["organizer"]
        except KeyError:
            pass
        try:
            self.slcr_event_id = i["slcr_event_id"]
        except KeyError:
            pass
        try:
            self.style = i["style"]
        except KeyError:
            pass
        if "encoding_print" in i and i["encoding_print"] is not None:
            self.encoding_print = i["encoding_print"]

        self.eff_year = self.date.year
        if self.date.month < 7:
            self.eff_year -= 1

        self.mass = True
        if "interval" in i:
            self.mass = False
            self.start = hooshek.util.util.parseTime(i["interval"]["start"])
            self.interval_race = datetime.timedelta(seconds=i["interval"]["race"])
            self.interval_athlete = datetime.timedelta(seconds=i["interval"]["athlete"])
            self.interval_groupby = i["interval"]["groupby"]

        self.races = tuple(hooshek.event.race.Race(x) for x in i["races"])

    def toString(self):
        return "Event name: {}, date: {}, effective year: {}, start: {}, mass: {}, interval_race: {}".format(
            self.name,
            self.date,
            self.eff_year,
            self.start if hasattr(self, "start") else "",
            self.mass,
            self.interval_race if hasattr(self, "interval_race") else "",
        )
