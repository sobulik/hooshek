#!/usr/bin/env python3

import json
from datetime import date, datetime

def dump(obj, ofile):
    """dump object as a json file"""
    with open(ofile, 'w', encoding="utf-8") as f:
        return json.dump(obj, f, indent=4, default=json_serial, ensure_ascii=False)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
