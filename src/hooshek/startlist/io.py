#!/usr/bin/env python3

import os

import hooshek.persistence.termtables
import hooshek.persistence.yaml


def load():
    """load start list"""
    if os.path.exists("start.yaml"):
        raw = hooshek.persistence.yaml.load("start.yaml")
    else:
        raw = None

    sanity_check(raw)

    return raw


def sanity_check(raw):
    pass


def dump(start, encoding_print):
    """write start list"""
    o = {}
    o["name"] = start["name"]
    o["date"] = start["date"]
    o["mass"] = start["mass"]
    o["races"] = []
    for race in start["races"]:
        r = {}
        r["name"] = race.name
        r["sex"] = race.sex
        r["distance"] = race.distance
        r["athletes"] = []
        for athlete in race.athletes:
            a = {}
            a["id"] = athlete.id
            a["name"] = athlete.name
            a["surname"] = athlete.surname
            a["born"] = athlete.born
            a["club"] = athlete.club.abb15 if athlete.club is not None else ""
            a["start"] = athlete.start.strftime("%H:%M:%S")
            r["athletes"].append(a)
        o["races"].append(r)

    hooshek.persistence.yaml.dump(o, "start.yaml")
    hooshek.persistence.termtables.dump_start(o, "start.txt", encoding_print)
