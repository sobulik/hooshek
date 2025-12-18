#!/usr/bin/env python3

import event.io
import athletes.io
import clubs.io
import start.io
import finish.io
import finish.category

import persistence.json
import persistence.yaml

import datetime

event = event.io.load()
clubs = clubs.io.load()
start = start.io.load()
flist = finish.io.load()

if __name__ == "__main__":

    aths = tuple(filter(lambda x: hasattr(x, "id"), athletes.io.build(clubs)))

    slcr = []
    i = 0
    for race in event.races:
        if race.age_max < 4:
            continue
        i += 1
        r = dict()
        for e in finish.category.eval_categories(event.eff_year, race, False):
            finish.category.fill_category(e, event, aths, race, start, flist)
            r["uniqueId"] = str(i)  # string # Interní ID závodu časoměřiče
            r["resultsLayout"] = "CROSS_COUNTRY_INDIVIDUAL_MASS_START" if event.mass else "CROSS_COUNTRY_INDIVIDUAL_DISTANCE"  # string # layout závodu, viz. Číselník
            r["categoryYearFrom"] = event.eff_year - race.age_max  # int # Kategorie ročník narození od
            r["categoryYearTo"] = event.eff_year - race.age_min  # int # Kategorie ročník narození do
            r["gender"] = race.sex.upper()  # string # Pohlaví M … muži, W / L / F … ženy
            r["registeredCount"] = len(e["started"])  # int # Počet přihlášených závodníků
            r["startedCount"] = len(e["started"])  # int # počet odstartovaných závodníků
            r["classifiedCount"] = len(e["finished"]) - len(e["unfinished"]) # int # Počet klasifikovaných závodníků
            r["dnsCount"] = 0  # int # Počet DNS závodníků
            r["dnfCount"] = len(e["unfinished"])  # int # Počet DNF závodníků
            r["dsqCount"] = 0  # int # Počet diskvalifikovaných závodníků
            r["dqbCount"] = 0  # int # Počet DQB závodníků
            r["npsCount"] = 0  # int # Počet NPS závodníků
            r["lapCount"] = 0  # int # Počet LAPnutých závodníků
            r["organizer"] = event.organizer  # string # Pořadatel závodu
            r["raceName"] = race.slcr_name  # string # Název závodu
            r["raceDateStart"] = datetime.datetime.combine(event.date, event.start) if hasattr(event, "start") else datetime.datetime.combine(event.date, datetime.time(10)) # string # Datum začátku závodu
            r["raceLocation"] = event.location  # string # Místo závodu
            r["trackLengthKm"] = float(race.distance.removesuffix("m")) / 1000  # float # Délka trati
            r["style"] = event.style if event.style is not None else "Přespolní běh"  # string # styl
            r["eventId"] = event.slcr_event_id  # int # SLČR ID události
            r["results"] = []  # array # výsledky individuálního závodu
            first_one = None
            for ath in e["athletes"]:
                a = dict()
                if hasattr(ath, "rank"):
                    a["rank"] = ath.rank
                a["lastName"] = ath.surname
                a["firstName"] = ath.name
                a["gender"] = ath.sex.upper()
                a["yearOfBirth"] = ath.born
                if ath.club is not None:
                    a["clubAbbreviation"] = ath.club.id
                    a["clubName"] = ath.club.name
                if hasattr(ath, "time"):
                    a["timeMilliseconds"] = ath.time // datetime.timedelta(milliseconds = 1)
                    if first_one is None:
                        first_one = a["timeMilliseconds"]
                    a["diffMilliseconds"] = a["timeMilliseconds"] - first_one
                r["results"].append(a)
            slcr.append(r)

    persistence.json.dump(slcr, "slcr-export.json")
