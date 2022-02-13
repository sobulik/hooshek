#!/usr/bin/env python3

import event
import clubs
import athletes

import collections
import hashlib

event = event.load()
clubs = clubs.load()

aths = athletes.build(clubs, False)
athsWithId = tuple(filter(lambda x: hasattr(x, "id"), aths))

# expect no id or id == "0"
idCounter = collections.Counter(map(lambda x: x.id, athsWithId))
for i in idCounter:
    if i != "0" and idCounter[i] > 0:
        raise Exception("Athletes file athlete id " + i + " defined " + str(idCounter[i]) + " times. Only zeros are expected!")

number_red = 0
number_black = 100
for race in event.races:
    raceAths = list()
    for athlete in athsWithId:
        if (athlete.sex == race.sex
                and event.eff_year - athlete.born >= race.age_min
                and event.eff_year - athlete.born <= race.age_max):
            raceAths.append((athlete, hashlib.md5("{0}{1}{2}".format(athlete.name, athlete.surname, event.date).encode()).hexdigest()))
    raceAths.sort(key=lambda t: t[1])
    for t in raceAths:
        if t[0].born > event.eff_year - 10:
            number_red += 1
            t[0].id = str(number_red)
        else:
            number_black += 1
            while number_black in (216, 235):
                number_black += 1
            t[0].id = str(number_black)

# assert
idCounter = collections.Counter(map(lambda x: x.id, athsWithId))
for i in idCounter:
    if i == "0":
        raise Exception("Athletes file athlete id " + i + " not numerated correctly")
    if idCounter[i] > 1:
        raise Exception("Athletes file athlete id " + i + " defined " + str(idCounter[i]) + " times")

athletes.dump(aths, "athletes-with-numbers.yaml")

#print("The last numbers assigned are {0} and {1}".format(str(number_red), str(number_black)))
