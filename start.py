#!/usr/bin/env python3

import event
import athletes
import start

import datetime

event = event.load()
aths = tuple(filter(lambda x: hasattr(x, "id"), athletes.load()))

startlist = dict()
startlist["name"] = event.name
startlist["date"] = event.date
startlist["races"] = list()

# set race athletes
for race in event.races:
    startlist["races"].append(race)
    race.athletes = list()
    for athlete in aths:
        if (athlete.sex == race.sex
                and event.eff_year - athlete.born >= race.age_min 
                and event.eff_year - athlete.born <= race.age_max):
            race.athletes.append(athlete)

# sort athletes
for race in startlist["races"]:
    race.athletes.sort(key=lambda athlete : athlete.id)

# set start times
if event.mass:
    for race in startlist["races"]:
        for athlete in race.athletes:
            athlete.start = datetime.time()
else:
    time = datetime.datetime.combine(event.date, event.start)
    for race in startlist["races"]:
        # override event defaults
        if hasattr(race, "start"):
            time = datetime.datetime.combine(event.date, race.start)
        interval = event.interval_athlete
        if hasattr(race, "interval_athlete"):
            interval = race.interval_athlete
        groupby = event.interval_groupby
        if hasattr(race, "interval_groupby"):
            groupby = race.interval_groupby

        group = 0
        for athlete in race.athletes:
            if group == groupby:
                time += interval
                group = 0
            athlete.start = datetime.datetime.fromtimestamp(time.timestamp())
            group += 1
        time += event.interval_race

start.dump(startlist)
