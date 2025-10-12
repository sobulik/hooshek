#!/usr/bin/env python3

import event.io
import athletes.io
import clubs.io
import start.io
import finish.io

import finish

event = event.io.load()
clubs = clubs.io.load()
start = start.io.load()
flist = finish.io.load()

if __name__ == "__main__":
    aths = tuple(filter(lambda x: hasattr(x, "id"), athletes.io.build(clubs)))
    results = dict()
    results["name"] = event.name
    results["date"] = event.date
    results["mass"] = event.mass
    results["evals"] = list()
    for race in event.races:
        for e in finish.eval_categories(event.eff_year, race, True):
            finish.fill_category(e, event, aths, race, start, flist)
            results["evals"].append(e)

    finish.io.dump(results, event.encoding_print)
