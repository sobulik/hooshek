#!/usr/bin/env python3

import event
import athletes
import clubs
import start
import finish

from util import util
import datetime

event = event.load()
clubs = clubs.load()
start = start.load()
flist = finish.load()

aths = tuple(filter(lambda x: hasattr(x, "id"), athletes.load()))
results = dict()
results["name"] = event.name
results["date"] = event.date
results["mass"] = event.mass
results["evals"] = list()
for race in event.races:
    evaluations = list()
    if hasattr(race, "eval"):
        for evaluation in race.eval:
            e = dict()
            e["age_min"] = evaluation["age_min"]
            e["age_max"] = evaluation["age_max"]
            if e["age_min"] == e["age_max"]:
                e["desc"] = str(event.eff_year - e["age_max"])
            else:
                e["desc"] = str(event.eff_year - e["age_max"]) + " - " + str(event.eff_year - e["age_min"])
            evaluations.append(e)
    else:
        e = dict()
        e["age_min"] = race.age_min
        e["age_max"] = race.age_max
        e["desc"] = ""
        evaluations.append(e)
    for e in evaluations:
        results["evals"].append(e)
        e["name"] = race.name
        e["sex"] = race.sex
        e["distance"] = race.distance

        e["athletes"] = list()
        for athlete in aths:
            if (athlete.sex == e["sex"]
                    and event.eff_year - athlete.born >= e["age_min"]
                    and event.eff_year - athlete.born <= e["age_max"]):
                e["athletes"].append(athlete)

        for athlete in e["athletes"]:
            for r in start["races"]:
                for a in r["athletes"]:
                    if athlete.id == a["id"]:
                        athlete.start = a["start"]
                        break
                if athlete.start is not None:
                    break
            result = list(filter(lambda x: x["id"] == athlete.id, flist))
            if (len(result) == 1 and athlete.start is not None):
                athlete.finish = util.parseTime(result[0]["time"])
                athlete.time = datetime.datetime.combine(event.date, athlete.finish) - datetime.datetime.combine(event.date, util.parseTime(athlete.start))

        finished = sorted(filter(lambda a: hasattr(a, "time"), e["athletes"]), key=lambda a: a.time)
        unfinished = sorted(filter(lambda a: not hasattr(a, "time"), e["athletes"]), key=lambda a: a.id)
        e["athletes"] = finished
        rank = 0
        rank_sokol = 0
        for athlete in e["athletes"]:
            rank += 1
            athlete.rank = rank
            if hasattr(athlete, "club") and athlete.club in clubs and clubs[athlete.club].isSokol:
                rank_sokol += 1
                athlete.rank_sokol = rank_sokol
        e["athletes"].extend(unfinished)

finish.dump(results, event.encoding_print)
