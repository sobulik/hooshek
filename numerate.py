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

# expect no id or id == 0
idCounter = collections.Counter(map(lambda x: x.id, athsWithId))
for i in idCounter:
    if i != 0 and idCounter[i] > 0:
        raise Exception("Athletes file athlete id " + str(i) + " defined " + str(idCounter[i]) + " times. Only zeros are expected!")

number = 0
for race in event.races:
    raceAths = list()
    for athlete in athsWithId:
        if (athlete.sex == race.sex
                and event.eff_year - athlete.born >= race.age_min
                and event.eff_year - athlete.born <= race.age_max):
            raceAths.append((athlete, hashlib.md5("{0}{1}{2}".format(athlete.name, athlete.surname, event.date).encode()).hexdigest()))
    raceAths.sort(key=lambda t: t[1])
    for t in raceAths:
        number += 1
        t[0].id = number

# assert
idCounter = collections.Counter(map(lambda x: x.id, athsWithId))
for i in idCounter:
    if i == 0:
        raise Exception("Athletes file athlete id " + str(i) + " not numerated correctly")
    if idCounter[i] > 1:
        raise Exception("Athletes file athlete id " + str(i) + " defined " + str(idCounter[i]) + " times")

athletes.dump(aths, "athletes-with-numbers.yaml")

#print("The last number assigned is {0}".format(str(number)))
