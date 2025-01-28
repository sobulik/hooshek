#!/usr/bin/env python3

import clubs.io
import athletes.io

import argparse
#import locale
import random

## locale.strxfrm(athlete.surname) fails on Mac with locale set
#try:
#    locale.setlocale(locale.LC_COLLATE, "cs_CZ.UTF-8")
#except locale.Error:
#    pass

clubs = clubs.io.load()
aths = athletes.io.build(clubs)
aths = sorted(aths, key=lambda athlete : athlete.surname)
aths = sorted(aths, key=lambda athlete : athlete.sex)
aths = sorted(aths, key=lambda athlete : athlete.born, reverse=True)

parser = argparse.ArgumentParser()
parser.add_argument("--shuffle", help="shuffle names to anonymize and store as file SHUFFLE")
args = parser.parse_args()

if args.shuffle:
    for athlete in aths:
        athlete.name = ''.join(random.sample(athlete.name, len(athlete.name))).lower().title()
        athlete.surname = ''.join(random.sample(athlete.surname, len(athlete.surname))).lower().title()
    athletes.io.dump(aths, args.shuffle)
else:
    athletes.io.dump(aths, "athletes-sorted.yaml")
