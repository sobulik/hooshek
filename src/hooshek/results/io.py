#!/usr/bin/env python3

import collections

import cerberus

import hooshek.persistence.termtables
import hooshek.persistence.yaml
import hooshek.util.util

from ..exceptions import ValidationError


def load():
    """return a list of finish times"""
    finish = hooshek.persistence.yaml.load("finish.yaml")
    finish = validate(finish)

    # primary key check
    idCounter = collections.Counter(x["id"] for x in finish)
    for i in idCounter:
        if idCounter[i] > 1:
            raise ValidationError(
                "Finish file result for id "
                + str(i)
                + " defined "
                + str(idCounter[i])
                + " times"
            )

    return tuple(finish)


def validate(raw):
    schema = {
        "aux": {
            "type": "list",
            "minlength": 1,
            "schema": {
                "type": "dict",
                "schema": {
                    "id": {"type": "string"},
                    "time": {
                        "type": "string",
                        "regex": "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9]$",
                    },
                },
            },
        }
    }

    v = cerberus.Validator(schema, require_all=True)
    d = {"aux": raw}
    if not v.validate(d):
        print(v.errors)
        raise ValidationError("Finish file does not validate")
    return v.document["aux"]


def dump(start, encoding_print):
    """write results"""
    o = {}
    o["name"] = start["name"]
    o["date"] = start["date"]
    o["races"] = []
    for race in start["evals"]:
        r = {}
        r["name"] = race["name"]
        r["desc"] = race["desc"]
        r["sex"] = race["sex"]
        r["distance"] = race["distance"]
        r["athletes"] = []
        first_one = (
            race["athletes"][0]
            if len(race["athletes"]) > 0 and hasattr(race["athletes"][0], "time")
            else None
        )
        for athlete in race["athletes"]:
            a = {}
            a["rank"] = athlete.rank if athlete.rank is not None else ""
            a["rank_sokol"] = (
                athlete.rank_sokol if athlete.rank_sokol is not None else ""
            )
            a["name"] = athlete.name
            a["surname"] = athlete.surname
            a["born"] = athlete.born
            a["club"] = athlete.club.abb15 if athlete.club is not None else ""
            a["start"] = athlete.start
            a["finish"] = (
                athlete.finish.strftime("%H:%M:%S")
                if athlete.finish is not None
                else ""
            )
            a["time"] = (
                hooshek.util.util.format_delta(athlete.time)
                if athlete.time is not None
                else ""
            )
            a["diff"] = (
                hooshek.util.util.format_delta(athlete.time - first_one.time)
                if athlete.time is not None and first_one is not None
                else ""
            )
            r["athletes"].append(a)
        o["races"].append(r)

    hooshek.persistence.yaml.dump(o, "results.yaml")
    hooshek.persistence.termtables.dump_finish(o, "results.txt", encoding_print)
