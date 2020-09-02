#!/usr/bin/env python3

from persistence import yaml
from .athlete import Athlete

import os

def load():
    """return a list of Athlete instances"""
    if os.path.exists("athletes.yaml"):
        raw = yaml.load("athletes.yaml")
    else:
        raw = None

    sanity_check(raw)

    return tuple(map(lambda x: Athlete(x), raw["athletes"]))

def sanity_check(raw):
    if raw is None:
        raise Exception("Athletes file not found")
    if "version" not in raw:
        raise Exception("Athletes file version missing")
    if raw["version"] != "1.0":
        raise Exception("Athetes file version " + raw["version"] + " not supported")
    if "athletes" not in raw:
        raise Exception("Athletes file athletes missing")
    if len(raw["athletes"]) == 0:
        raise Exception("Athletes file athletes empty")
    for athlete in raw["athletes"]:
        if "name" not in athlete:
            raise Exception("Missing name for an athlete")
        if "surname" not in athlete:
            raise Exception("Missing surname for an athlete")
        if "born" not in athlete:
            raise Exception("Missing born field for an athlete")
        if "sex" not in athlete:
            raise Exception("Missing sex field for an athlete")
        if athlete["sex"] not in ("f", "m"):
            raise Exception("Invalid sex field for an athlete")
        
    # primary key check
    ids = list(map(lambda x: x["id"], filter(lambda x: "id" in x, raw["athletes"])))
    for i in ids:
        if ids.count(i) > 1:
            raise Exception("Athletes file athlete id " + str(i) + " defined " + str(ids.count(i)) + " times")
    # unique key check
    uniquekeys = list(map(lambda x: (x["name"], x["surname"], x["born"]), raw["athletes"]))
    for i in uniquekeys:
        if uniquekeys.count(i) > 1:
            raise Exception("Athletes file athlete " + str(i) + " defined " + str(uniquekeys.count(i)) + " times")

def dump(athletes, filename="athletes-sorted.yaml"):
    """write athletes"""
    o = dict()
    o["version"] = "1.0"
    o["athletes"] = list()
    for athlete in athletes:
        a = dict()
        if hasattr(athlete, "id"):
            a["id"] = athlete.id
        a["name"] = athlete.name
        a["surname"] = athlete.surname
        a["born"] = athlete.born
        a["sex"] = athlete.sex
        a["club"] = athlete.club
        o["athletes"].append(a)
        
    yaml.dump(o, filename)
