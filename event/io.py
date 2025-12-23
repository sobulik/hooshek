#!/usr/bin/env python3

import persistence.yaml
import event.event

import cerberus

import collections
import copy
import datetime
import os

def load():
    """return Event instance"""
    ivent = persistence.yaml.load("event.yaml")
    ivent = validate(ivent)

    # unique key check
    uniqueCounter = collections.Counter(map(lambda x: (x["age_min"], x["age_max"], x["sex"]), ivent["races"]))
    for i in uniqueCounter:
        if uniqueCounter[i] > 1:
            raise Exception("Event file race " + str(i) + " defined " + str(uniqueCounter[i]) + " times")

    for race in ivent["races"]:
        if (int(race["age_min"]) > int(race["age_max"])):
            raise Exception("age_min higher than age_max for a race")

        if "eval" in race:
            for e in race["eval"]:
                if (int(e["age_min"]) > int(e["age_max"])):
                    raise Exception("age_min higher than age_max for an evaluation")
                if (int(e["age_min"]) < int(race["age_min"])):
                    raise Exception("age_min in evaluation lower than age_min for a race")
                if (int(e["age_max"]) > int(race["age_max"])):
                    raise Exception("age_max in evaluation higher than age_max for a race")
        
    return event.event.Event(ivent)

def validate(raw):
    schema_1_0 = {
        "version": {
            "type": "string",
            "allowed": ["1.0"]
        },
        "date": {
            "type": "date"
        },
        "encoding_print": {
            "type": "string",
            "required": False
        },
        "interval": {
            "type": "dict",
            "schema": {
                "start": {
                    "type": "string",
                    "regex": "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$"
                },
                "race": {
                    "type": "integer",
                    "min": 1
                },
                "athlete": {
                    "type": "integer",
                    "min": 1
                },
                "groupby": {
                    "type": "integer",
                    "min": 1
                }
            },
            "required": False
        },
        "name": {
            "type": "string"
        },
        "races": {
            "type": "list",
            "minlength": 1,
            "schema": {
                "type": "dict",
                "schema": {
                    "age_min": {
                        "type": "integer",
                        "min": 0
                    },
                    "age_max": {
                        "type": "integer",
                        "min": 0
                    },
                    "eval": {
                        "type": "list",
                        "minlength": 1,
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "age_min": {
                                    "type": "integer",
                                    "min": 0
                                },
                                "age_max": {
                                    "type": "integer",
                                    "min": 0
                                }
                            }
                        },
                        "required": False
                    },
                    "distance": {
                        "type": "string"
                    },
                    "interval": {
                        "type": "dict",
                        "schema": {
                            "start": {
                                "type": "string",
                                "regex": "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$"
                            },
                            "athlete": {
                                "type": "integer",
                                "min": 1
                            },
                            "groupby": {
                                "type": "integer",
                                "min": 1
                            }
                        },
                        "required": False
                    },
                    "name": {
                        "type": "string"
                    },
                    "sex": {
                        "type": "string",
                        "allowed": ["f", "m"]
                    },
                    "start": {
                        "type": "string",
                        "regex": "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$",
                        "required": False
                    }
                }
            }
        }
    }
    schema_1_1 = copy.deepcopy(schema_1_0)
    schema_1_1["version"]["allowed"] = ["1.1"]
    schema_1_1["location"] = {
        "type": "string"
    }
    schema_1_1["organizer"] = {
        "type": "string"
    }
    schema_1_1["races"]["schema"]["schema"]["slcr_name"] = {
        "type": "string",
        "required": False
    }
    schema_1_1["slcr_event_id"] = {
        "type": "integer"
    }
    schema_1_1["style"] = {
        "type": "string",
        "allowed": ["Přespolní běh", "klasicky", "volně"]
    }

    val_result = None
    for schema in (schema_1_0, schema_1_1):
        v = cerberus.Validator(schema, require_all=True)
        val_result = (schema, v, False)
        if v.validate(raw):
            val_result = (schema, v, True)
            break
    if not val_result[2]:
        print(val_result[1].errors)
        raise Exception("Event file does not validate")
    return val_result[1].document
