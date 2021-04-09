#!/usr/bin/env python3

import clubs
import athletes

import argparse
import locale
import random

try:
    locale.setlocale(locale.LC_COLLATE, "cs_CZ.utf8")
except locale.Error:
    pass

clubs = clubs.load()
aths = athletes.build(clubs)
aths = sorted(aths, key=lambda athlete : locale.strxfrm(athlete.surname))
aths = sorted(aths, key=lambda athlete : athlete.sex)
aths = sorted(aths, key=lambda athlete : athlete.born, reverse=True)

parser = argparse.ArgumentParser()
parser.add_argument("--shuffle", help="shuffle names to anonymize and store as file SHUFFLE")
parser.add_argument("--renumber", help="renumber ids based on default sort and store as file RENUMBER")
args = parser.parse_args()

if args.shuffle:
    for athlete in aths:
        athlete.name = ''.join(random.sample(athlete.name, len(athlete.name))).lower().title()
        athlete.surname = ''.join(random.sample(athlete.surname, len(athlete.surname))).lower().title()
    athletes.dump(aths, args.shuffle)
else:
    athletes.dump(aths)
