#!/usr/bin/env python3

import hooshek.event.io
import hooshek.clubs.repo
import hooshek.athletes.io

import collections
import hashlib

event = hooshek.event.io.load()
clubs = hooshek.clubs.repo.load()

aths = hooshek.athletes.io.build(clubs, False)
athsWithId = tuple(filter(lambda x: hasattr(x, "id"), aths))

# expect no id or id == "0"
idCounter = collections.Counter(map(lambda x: x.id, athsWithId))
for i in idCounter:
    if i != "0" and idCounter[i] > 0:
        raise Exception(
            "Athletes file athlete id "
            + i
            + " defined "
            + str(idCounter[i])
            + " times. Only zeros are expected!"
        )

bib_red = 0
bib_black = 100
for race in event.races:
    raceAths = list()
    for athlete in athsWithId:
        if (
            athlete.sex == race.sex
            and event.eff_year - athlete.born >= race.age_min
            and event.eff_year - athlete.born <= race.age_max
        ):
            raceAths.append(
                (
                    athlete,
                    hashlib.md5(
                        "{0}{1}{2}".format(
                            athlete.name, athlete.surname, event.date
                        ).encode()
                    ).hexdigest(),
                )
            )
    raceAths.sort(key=lambda t: t[1])
    for t in raceAths:
        if t[0].born > event.eff_year - 10:
            bib_red += 1
            t[0].id = str(bib_red)
        else:
            bib_black += 1
            while bib_black in (25, 235):
                bib_black += 1
            t[0].id = str(bib_black)

# assert
idCounter = collections.Counter(map(lambda x: x.id, athsWithId))
for i in idCounter:
    if i == "0":
        raise Exception("Athletes file athlete id " + i + " not numerated correctly")
    if idCounter[i] > 1:
        raise Exception(
            "Athletes file athlete id " + i + " defined " + str(idCounter[i]) + " times"
        )

hooshek.athletes.io.dump(aths, "athletes-with-bibs.yaml")

# print("The last bibs assigned are {0} and {1}".format(str(bib_red), str(bib_black)))
