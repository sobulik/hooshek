#!/usr/bin/env python3

import persistence.yaml
import athletes.athlete

import cerberus

import collections
import os

def build(clubs, primaryKeyCheck=True):
    """return a list of Athlete instances"""
    athletez = persistence.yaml.load("athletes.yaml")
    athletez = validate(athletez)

    # primary key check
    if primaryKeyCheck:
        idCounter = collections.Counter(map(lambda x: x["id"], filter(lambda x: "id" in x, athletez["athletes"])))
        for i in idCounter:
            if idCounter[i] > 1:
                raise Exception("Athletes file athlete id " + str(i) + " defined " + str(idCounter[i]) + " times")

    # unique key check
    uniqueCounter = collections.Counter(map(lambda x: (x["name"], x["surname"], x["born"]), athletez["athletes"]))
    for i in uniqueCounter:
        if uniqueCounter[i] > 1:
            raise Exception("Athletes file athlete " + str(i) + " defined " + str(uniqueCounter[i]) + " times")

    # associate clubs
    for a in athletez["athletes"]:
        if "club" in a:
            if a["club"] in clubs:
                a["club"] = clubs[a["club"]]
            else:
                raise Exception("Club " + a["club"] + " of athlete " + a["surname"] + "not defined in clubs")

    return tuple(map(lambda x: athletes.athlete.Athlete(x), athletez["athletes"]))

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
                        "type": "string",
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

    v = cerberus.Validator(schema, require_all=True)
    if not v.validate(raw):
        print(v.errors)
        raise Exception("Athletes file does not validate")
    return v.document

def dump(athletes, filename):
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
        
    persistence.yaml.dump(o, filename)
