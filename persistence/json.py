#!/usr/bin/env python3

import json
from datetime import date, datetime

def dump(obj, ofile, encoding_print):
    """dump results to a json file"""
    with open(ofile, 'w', encoding=encoding_print) as f:
        json.dump(obj, f, indent=2, default=json_serial, ensure_ascii=False)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
