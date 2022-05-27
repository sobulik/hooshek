#!/usr/bin/env python3

import event.io
import clubs.io
import athletes.io
from athletes.athlete import Athlete

import collections
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("file", help="csv file to register")
args = parser.parse_args()

event = event.io.load()
clubs = clubs.io.load()

aths = list(athletes.io.build(clubs, False))

with open(args.file, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        year = int(row[3])
        present = False
        for a in aths:
            if row[1] == a.name and row[0] == a.surname and year == a.born:
                present = True
                if len(row) > 4:
                    if row[4] in clubs:
                        a.club = clubs[row[4]]
                    else:
                        raise Exception("Club " + row[4] + " of athlete " + row[0] + " not defined in clubs")
                a.id = "0"
                print("{0} already present".format(row))
                break
        if not present:
            club = None
            if len(row) > 4:
                if row[4] in clubs:
                    club = clubs[row[4]]
                else:
                    raise Exception("Club " + row[4] + " of athlete " + row[0] + " not defined in clubs")
            a = Athlete({"id": "0", "name": row[1], "surname": row[0], "born": year, "sex": row[2], "club": club})
            aths.append(a)
            print("{0} created".format(row))

athletes.io.dump(aths, "athletes-with-external.yaml")
