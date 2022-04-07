#!/usr/bin/env python3

import persistence.yaml
import persistence.termtables
import util.util

import cerberus

import collections
import datetime
import os

def load():
    """return a list of finish times"""
    finish = persistence.yaml.load("finish.yaml")
    finish = validate(finish)
        
    # primary key check
    idCounter = collections.Counter(map(lambda x: x["id"], finish))
    for i in idCounter:
        if idCounter[i] > 1:
            raise Exception("Finish file result for id " + str(i) + " defined " + str(idCounter[i]) + " times")

    return tuple(finish)

def validate(raw):
    schema = {
        "aux": {
            "type": "list",
            "minlength": 1,
            "schema": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "string"
                    },
                    "time": {
                        "type": "string",
                        "regex": "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9]$"
                    }
                }
            }
        }
    }

    v = cerberus.Validator(schema, require_all=True)
    d = {"aux": raw}
    if not v.validate(d):
        print(v.errors)
        raise Exception("Finish file does not validate")
    return v.document["aux"]

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
            a["club"] = athlete.club.abb15 if athlete.club is not None else ""
            a["start"] = athlete.start
            a["finish"] = athlete.finish.strftime("%H:%M:%S") if hasattr(athlete, "finish") and athlete.finish is not None else ""
            a["time"] = util.util.format_delta(athlete.time) if hasattr(athlete, "time") and athlete.time is not None else ""
            a["diff"] = util.util.format_delta(athlete.time - first_one.time) if hasattr(athlete, "time") and first_one is not None else ""
            r["athletes"].append(a)
        o["races"].append(r)
        
    persistence.yaml.dump(o, "results.yaml")
    persistence.termtables.dump_finish(o, "results.txt", encoding_print)
