#!/usr/bin/env python3

import hooshek.event.io
import hooshek.athletes.io
import hooshek.clubs.repo
import hooshek.startlist.io
import hooshek.results.io
import hooshek.results.category

event = hooshek.event.io.load()
clubs = hooshek.clubs.repo.load()
start = hooshek.startlist.io.load()
flist = hooshek.results.io.load()

if __name__ == "__main__":
    aths = tuple(filter(lambda x: hasattr(x, "id"), hooshek.athletes.io.build(clubs)))
    results = dict()
    results["name"] = event.name
    results["date"] = event.date
    results["mass"] = event.mass
    results["evals"] = list()
    for race in event.races:
        for e in hooshek.results.category.eval_categories(event.eff_year, race, True):
            hooshek.results.category.fill_category(e, event, aths, race, start, flist)
            results["evals"].append(e)

    hooshek.results.io.dump(results, event.encoding_print)
