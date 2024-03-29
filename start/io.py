#!/usr/bin/env python3

import persistence.yaml
import persistence.termtables

import os

def load():
    """load start list"""
    if os.path.exists("start.yaml"):
        raw = persistence.yaml.load("start.yaml")
    else:
        raw = None

    sanity_check(raw)

    return raw

def sanity_check(raw):
    pass

def dump(start, encoding_print):
    """write start list"""
    o = dict()
    o["name"] = start["name"]
    o["date"] = start["date"]
    o["mass"] = start["mass"]
    o["races"] = list()
    for race in start["races"]:
        r = dict()
        r["name"] = race.name
        r["sex"] = race.sex
        r["distance"] = race.distance
        r["athletes"] = list()
        for athlete in race.athletes:
            a = dict()
            a["id"] = athlete.id
            a["name"] = athlete.name
            a["surname"] = athlete.surname
            a["born"] = athlete.born
            a["club"] = athlete.club.abb15 if athlete.club is not None else ""
            a["start"] = athlete.start.strftime("%H:%M:%S")
            r["athletes"].append(a)
        o["races"].append(r)
        
    persistence.yaml.dump(o, "start.yaml")
    persistence.termtables.dump_start(o, "start.txt", encoding_print)
