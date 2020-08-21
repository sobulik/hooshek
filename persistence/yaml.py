#!/usr/bin/env python3

import yaml

def load(ifile):
    """load yaml from an input file"""
    with open(ifile, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def dump(obj, ofile):
    """dump yaml to an output file"""
    with open(ofile, "w", encoding="utf-8") as f:
        return yaml.safe_dump(obj, f, allow_unicode=True, indent=4)
