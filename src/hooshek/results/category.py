import dataclasses
import datetime

from hooshek.util import util


def eval_categories(eff_year, race, fine):
    eval_categories = []
    if fine and hasattr(race, "eval"):
        for evaluation in race.eval:
            e = {}
            e["age_min"] = evaluation["age_min"]
            e["age_max"] = evaluation["age_max"]
            if e["age_min"] == e["age_max"]:
                e["desc"] = str(eff_year - e["age_max"])
            else:
                e["desc"] = (
                    str(eff_year - e["age_max"]) + " - " + str(eff_year - e["age_min"])
                )
            eval_categories.append(e)
    else:
        e = {}
        e["age_min"] = race.age_min
        e["age_max"] = race.age_max
        e["desc"] = ""
        eval_categories.append(e)
    return eval_categories


def fill_category(e, event, aths, race, start, flist):
    e["name"] = race.name
    e["sex"] = race.sex
    e["distance"] = race.distance

    e["started"] = []
    for athlete in aths:
        if (
            athlete.sex == e["sex"]
            and event.eff_year - athlete.born >= e["age_min"]
            and event.eff_year - athlete.born <= e["age_max"]
        ):
            e["started"].append(athlete)

    for i, athlete in enumerate(e["started"]):
        for r in start["races"]:
            for a in r["athletes"]:
                if athlete.id == a["id"]:
                    e["started"][i] = dataclasses.replace(
                        e["started"][i], start=a["start"]
                    )
                    break
            if e["started"][i].start is not None:
                break
        result = list(filter(lambda x: x["id"] == e["started"][i].id, flist))
        if (
            len(result) == 1
            and e["started"][i].start is not None
            and result[0]["time"] != "00:00:00.0"
        ):
            e["started"][i] = dataclasses.replace(
                e["started"][i], finish=util.parseTime(result[0]["time"])
            )
            tt = datetime.datetime.combine(
                event.date, e["started"][i].finish
            ) - datetime.datetime.combine(
                event.date, util.parseTime(e["started"][i].start)
            )
            if not event.mass and event.version != "1.0":
                tt += datetime.timedelta(
                    hours=event.start.hour,
                    minutes=event.start.minute,
                    seconds=event.start.second,
                )
            e["started"][i] = dataclasses.replace(e["started"][i], time=tt)

    e["finished"] = sorted(
        filter(lambda a: a.time is not None, e["started"]), key=lambda a: a.time
    )
    e["unfinished"] = sorted(
        filter(lambda a: a.time is None, e["started"]),
        key=lambda a: a.id if a.id is not None else "",
    )
    e["athletes"] = e["finished"]
    rank_sokol = 0
    for rank, athlete in enumerate(e["athletes"]):
        e["athletes"][rank] = dataclasses.replace(athlete, rank=rank + 1)
        if athlete.club is not None and athlete.club.is_sokol:
            rank_sokol += 1
            e["athletes"][rank] = dataclasses.replace(
                e["athletes"][rank], rank_sokol=rank_sokol
            )
    e["athletes"].extend(e["unfinished"])
