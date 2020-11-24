#!/usr/bin/env python3

from persistence import yaml
from .club import Club

import os

def load():
    """return a dictionary of Club instances"""
    if os.path.exists("clubs.yaml"):
        raw = yaml.load("clubs.yaml")
    else:
        raw = None

    sanity_check(raw)

    return {c.id: c for c in map(lambda x: Club(x), raw["clubs"])}

def sanity_check(raw):
    if raw is None:
        raise Exception("Clubs file not found")
    if "version" not in raw:
        raise Exception("Clubs file version missing")
    if raw["version"] != "1.0":
        raise Exception("Clubs file version " + raw["version"] + " not supported")
    if "clubs" not in raw:
        raise Exception("Clubs file clubs missing")
    if len(raw["clubs"]) == 0:
        raise Exception("Clubs file clubs empty")
    ids = list(map(lambda x: x["id"], raw["clubs"]))
    for i in ids:
        if i is None:
            raise Exception("Clubs file club id missing")
        if ids.count(i) > 1:
            raise Exception("Clubs file club id " + i + " defined " + str(ids.count(i)) + " times")
    for club in raw["clubs"]:
        if not "abb15" in club:
            raise Exception("No abb15 for club " + club["id"])
        else:
            if len(club["abb15"]) > 15:
                raise Exception("Clubs abb " + club["abb15"] + " is " + str(len(club["abb15"])) + " chars long")
