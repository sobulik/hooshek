#!/usr/bin/env python3

import event
import clubs
import athletes
import start

import argparse
import datetime
import string

event = event.load()
clubs = clubs.load()
aths = tuple(filter(lambda x: hasattr(x, "id"), athletes.build(clubs)))

startlist = dict()
startlist["name"] = event.name
startlist["date"] = event.date
startlist["mass"] = event.mass
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

def comparator(a):
    if a.id.startswith(tuple(string.ascii_uppercase)):
        return a.id[0] + a.id[1:].rjust(3, "0")
    return a.id.rjust(3, "0")

# sort athletes
for race in startlist["races"]:
    race.athletes.sort(key=comparator)

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

start.dump(startlist, event.encoding_print)

parser = argparse.ArgumentParser()
parser.add_argument("--clubs", help="print startlist grouped by club", action="store_true")
args = parser.parse_args()

if args.clubs:
    aths = list()
    for race in startlist["races"]:
        for athlete in race.athletes:
            if athlete.club is not None:
                aths.append(athlete)
    aths = sorted(aths, key=comparator)
    aths = sorted(aths, key=lambda athlete : athlete.club.id)
    club = ""
    with open("start-clubs.txt", "w", encoding=event.encoding_print) as f:
        for athlete in aths:
            if club != athlete.club.id:
                f.write("\n\n--------------------------------------------------------------------\n\n")
                club = athlete.club.id
            f.write(athlete.toString())
            f.write("\n")
