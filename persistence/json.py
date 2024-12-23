#!/usr/bin/env python3

import json

def dump(obj, ofile, encoding_print):
    """dump results to a json file"""
    with open(ofile, 'w', encoding=encoding_print) as f:
        json.dump(obj, f, indent=2)
