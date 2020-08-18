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
results = start.load()
flist = finish.load()

for race in results["races"]:
    for athlete in race["athletes"]:
        result = list(filter(lambda x: x["id"] == athlete["id"], flist))
        if (len(result) == 1):
            athlete["finish"] = util.parseTime(result[0]["time"])
            athlete["time"] = datetime.datetime.combine(event.date, athlete["finish"]) - datetime.datetime.combine(event.date, util.parseTime(athlete["start"]))

    finished = sorted(filter(lambda a: "time" in a, race["athletes"]), key=lambda a: a["time"])
    unfinished = sorted(filter(lambda a: "time" not in a, race["athletes"]), key=lambda a: a["id"])
    race["athletes"] = finished
    rank = 0
    rank_sokol = 0
    for athlete in race["athletes"]:
        rank += 1
        athlete["rank"] = rank
        if "club" in athlete and athlete["club"] in clubs and clubs[athlete["club"]].isSokol:
            rank_sokol += 1
            athlete["rank_sokol"] = rank_sokol
    race["athletes"].extend(unfinished)    

finish.dump(results)
