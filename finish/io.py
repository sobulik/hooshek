#!/usr/bin/env python3

from persistence import yaml
from persistence import termtables
from util import util

import datetime
import os

def load():
    """return a list of finish times"""
    if os.path.exists("finish.yaml"):
        raw = yaml.load("finish.yaml")
    else:
        raw = None

    sanity_check(raw)

    return tuple(raw)

def sanity_check(raw):
    if raw is None:
        raise Exception("Finish file not found")
    if len(raw) == 0:
        raise Exception("Finish file empty")
    for result in raw:
        if "id" not in result:
            raise Exception("Missing id for a result")
        if "time" not in result:
            raise Exception("Missing time for a result")
        try:
            util.parseTime(result["time"])
        except (ValueError, IndexError):
            raise Exception("Invalid time value in finish file")
        
    # primary key check
    ids = list(map(lambda x: x["id"], raw))
    for i in ids:
        if ids.count(i) > 1:
            raise Exception("Finish file result for id " + str(i) + " defined " + str(ids.count(i)) + " times")

def dump(start, encoding_print):
    """write results"""
    o = dict()
    o["name"] = start["name"]
    o["date"] = start["date"]
    o["races"] = list()
    for race in start["evals"]:
        r = dict()
        r["name"] = race["name"]
        r["desc"] = race["desc"]
        r["sex"] = race["sex"]
        r["distance"] = race["distance"]
        r["athletes"] = list()
        first_one = race["athletes"][0] if len(race["athletes"]) > 0 and hasattr(race["athletes"][0], "time") else None
        for athlete in race["athletes"]:
            a = dict()
            a["rank"] = athlete.rank if hasattr(athlete, "rank") else ""
            a["rank_sokol"] = athlete.rank_sokol if hasattr(athlete, "rank_sokol") else ""
            a["name"] = athlete.name
            a["surname"] = athlete.surname
            a["born"] = athlete.born
            a["club"] = athlete.club.id if athlete.club is not None else ""
            a["start"] = athlete.start
            a["finish"] = athlete.finish.strftime("%H:%M:%S") if hasattr(athlete, "finish") and athlete.finish is not None else ""
            a["time"] = util.format_delta(athlete.time) if hasattr(athlete, "time") and athlete.time is not None else ""
            a["diff"] = util.format_delta(athlete.time - first_one.time) if hasattr(athlete, "time") and first_one is not None else ""
            r["athletes"].append(a)
        o["races"].append(r)
        
    yaml.dump(o, "results.yaml")
    termtables.dump_finish(o, "results.txt", encoding_print)
