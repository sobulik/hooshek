from util import util
import datetime

def eval_categories(eff_year, race, fine):
    eval_categories = list()
    if fine and hasattr(race, "eval"):
        for evaluation in race.eval:
            e = dict()
            e["age_min"] = evaluation["age_min"]
            e["age_max"] = evaluation["age_max"]
            if e["age_min"] == e["age_max"]:
                e["desc"] = str(eff_year - e["age_max"])
            else:
                e["desc"] = str(eff_year - e["age_max"]) + " - " + str(eff_year - e["age_min"])
            eval_categories.append(e)
    else:
        e = dict()
        e["age_min"] = race.age_min
        e["age_max"] = race.age_max
        e["desc"] = ""
        eval_categories.append(e)
    return eval_categories

def fill_category(e, event, aths, race, start, flist):
    e["name"] = race.name
    e["sex"] = race.sex
    e["distance"] = race.distance

    e["started"] = list()
    for athlete in aths:
        if (athlete.sex == e["sex"]
                and event.eff_year - athlete.born >= e["age_min"]
                and event.eff_year - athlete.born <= e["age_max"]):
            e["started"].append(athlete)

    for athlete in e["started"]:
        for r in start["races"]:
            for a in r["athletes"]:
                if athlete.id == a["id"]:
                    athlete.start = a["start"]
                    break
            if athlete.start is not None:
                break
        result = list(filter(lambda x: x["id"] == athlete.id, flist))
        if (len(result) == 1 and athlete.start is not None and result[0]["time"] != "00:00:00.0"):
            athlete.finish = util.parseTime(result[0]["time"])
            athlete.time = datetime.datetime.combine(event.date, athlete.finish) - datetime.datetime.combine(event.date, util.parseTime(athlete.start))
            if not event.mass and event.version != "1.0":
                athlete.time += datetime.timedelta(hours=event.start.hour, minutes=event.start.minute, seconds=event.start.second)


    e["finished"] = sorted(filter(lambda a: hasattr(a, "time"), e["started"]), key=lambda a: a.time)
    e["unfinished"] = sorted(filter(lambda a: not hasattr(a, "time"), e["started"]), key=lambda a: a.id)
    e["athletes"] = e["finished"]
    rank = 0
    rank_sokol = 0
    for athlete in e["athletes"]:
        rank += 1
        athlete.rank = rank
        if athlete.club is not None and athlete.club.isSokol:
            rank_sokol += 1
            athlete.rank_sokol = rank_sokol
    e["athletes"].extend(e["unfinished"])
