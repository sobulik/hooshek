#!/usr/bin/env python3

from persistence import yaml
from .athlete import Athlete

from cerberus import Validator

import os

def build(clubs):
    """return a list of Athlete instances"""
    athletes = yaml.load("athletes.yaml")
    athletes = validate(athletes)

    # primary key check
    ids = list(map(lambda x: x["id"], filter(lambda x: "id" in x, athletes["athletes"])))
    for i in ids:
        if ids.count(i) > 1:
            raise Exception("Athletes file athlete id " + str(i) + " defined " + str(ids.count(i)) + " times")

    # unique key check
    uniquekeys = list(map(lambda x: (x["name"], x["surname"], x["born"]), athletes["athletes"]))
    for i in uniquekeys:
        if uniquekeys.count(i) > 1:
            raise Exception("Athletes file athlete " + str(i) + " defined " + str(uniquekeys.count(i)) + " times")

    # associate clubs
    for a in athletes["athletes"]:
        if "club" in a:
            if a["club"] in clubs:
                a["club"] = clubs[a["club"]]
            else:
                raise Exception("Club " + a["club"] + " of athlete " + a["surname"] + "not defined in clubs")

    return tuple(map(lambda x: Athlete(x), athletes["athletes"]))

def validate(raw):
    schema = {
        "version": {
            "type": "string",
            "allowed": ["1.0"]
        },
        "athletes": {
            "type": "list",
            "minlength": 1,
            "schema": {
                "type": "dict",
                "schema": {
                    "born": {
                        "type": "integer",
                        "min": 1900,
                        "max": 2100
                    },
                    "club": {
                        "type": "string",
                        "minlength": 4,
                        "maxlength": 4,
                        "required": False
                    },
                    "id": {
                        "type": "integer",
                        "required": False
                    },
                    "name": {
                        "type": "string"
                    },
                    "sex": {
                        "type": "string",
                        "allowed": ["f", "m"]
                    },
                    "surname": {
                        "type": "string"
                    }
                }
            }
        }
    }

    v = Validator(schema, require_all=True)
    if not v.validate(raw):
        print(v.errors)
        raise Exception("Athletes file does not validate")
    return v.document

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
        if athlete.club is not None:
            a["club"] = athlete.club.id
        o["athletes"].append(a)
        
    yaml.dump(o, filename)
