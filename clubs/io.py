#!/usr/bin/env python3

from persistence import yaml
from .club import Club

from cerberus import Validator

import collections
import os

def load():
    """return a dictionary of Club instances"""
    clubs = yaml.load("clubs.yaml")
    clubs = validate(clubs)

    # primary key check
    idCounter = collections.Counter(map(lambda x: x["id"], clubs["clubs"]))
    for i in idCounter:
        if idCounter[i] > 1:
            raise Exception("Clubs file club id " + i + " defined " + str(idCounter[i]) + " times")

    return {c.id: c for c in map(lambda x: Club(x), clubs["clubs"])}

def validate(raw):
    schema = {
        "version": {
            "type": "string",
            "allowed": ["1.0"]
        },
        "clubs": {
            "type": "list",
            "minlength": 1,
            "schema": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "string",
                        "minlength": 4,
                        "maxlength": 4
                    },
                    "name": {
                        "type": "string"
                    },
                    "abb15": {
                        "type": "string",
                        "maxlength": 15
                    },
                    "isSokol": {
                        "type": "boolean",
                        "required": False
                    }
                }
            }
        }
    }

    v = Validator(schema, require_all=True)
    if not v.validate(raw):
        print(v.errors)
        raise Exception("Clubs file does not validate")
    return v.document
