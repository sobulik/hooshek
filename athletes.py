#!/usr/bin/env python3

import athletes
import locale

try:
    locale.setlocale(locale.LC_COLLATE, "cs_CZ.utf8")
except locale.Error:
    pass

aths = athletes.load()
aths = sorted(aths, key=lambda athlete : locale.strxfrm(athlete.surname))
aths = sorted(aths, key=lambda athlete : athlete.sex)
aths = sorted(aths, key=lambda athlete : athlete.born, reverse=True)

#for athlete in aths:
    #print(athlete.toString())

athletes.dump(aths)
