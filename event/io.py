#!/usr/bin/env python3

from persistence import yaml
from util import util
from .event import Event

import datetime
import os

def load():
    """return Event instance"""
    if os.path.exists("event.yaml"):
        raw = yaml.load("event.yaml")
    else:
        raw = None

    sanity_check(raw)

    return Event(raw)

def sanity_check(raw):
    if raw is None:
        raise Exception("Event file not found")
    if "version" not in raw:
        raise Exception("Event file version missing")
    if raw["version"] != "1.0":
        raise Exception("Event file version " + raw["version"] + " not supported")
    if "name" not in raw:
        raise Exception("Event file name missing")
    if "date" not in raw:
        raise Exception("Event file date missing")
    if "interval" in raw:
        if "start" not in raw["interval"]:
            raise Exception("Event file start missing")
        try:
            util.parseTime(raw["interval"]["start"])
        except (ValueError):
            raise Exception("Invalid start value")
        if "race" not in raw["interval"]:
            raise Exception("Event file interval race missing")
        try:
            int(raw["interval"]["race"])
        except ValueError:
            raise Exception("Invalid interval race value")
        if "athlete" not in raw["interval"]:
            raise Exception("Event file interval athlete missing")
        try:
            int(raw["interval"]["athlete"])
        except ValueError:
            raise Exception("Invalid interval athlete value")
        try:
            int(raw["interval"]["groupby"])
        except ValueError:
            raise Exception("Invalid interval groupby value")
    if "races" not in raw:
        raise Exception("Event file races missing")
    if len(raw["races"]) == 0:
        raise Exception("Event file races empty")
    for race in raw["races"]:
        if "age_min" not in race:
            raise Exception("Missing age_min for a race")
        if "age_max" not in race:
            raise Exception("Missing age_max for a race")
        if "sex" not in race:
            raise Exception("Missing sex for a race")
        if "name" not in race:
            raise Exception("Missing name for a race")
        if "distance" not in race:
            raise Exception("Missing distance for a race")
        try:
            int(race["age_min"])
        except ValueError:
            raise Exception("Invalid age_min value for a race")
        try:
            int(race["age_max"])
        except ValueError:
            raise Exception("Invalid age_max value for a race")
        if (int(race["age_min"]) > int(race["age_max"])):
            raise Exception("age_min higher than age_max for a race")
        if race["sex"] not in ("f", "m"):
            raise Exception("Invalid sex value for a race")
        if "interval" in raw:
            if "start" in race:
                try:
                    util.parseTime(race["start"])
                except (ValueError):
                    raise Exception("Invalid start value for a race")
            if "athlete" in race:
                try:
                    int(race["athlete"])
                except ValueError:
                    raise Exception("Invalid interval for a race")
            if "groupby" in race:
                try:
                    int(race["groupby"])
                except ValueError:
                    raise Exception("Invalid groouby for a race")
        
    # unique key check
    uniquekeys = list(map(lambda x: (x["age_min"], x["age_max"], x["sex"]), raw["races"]))
    for i in uniquekeys:
        if uniquekeys.count(i) > 1:
            raise Exception("Event file race " + str(i) + " defined " + str(uniquekeys.count(i)) + " times")
