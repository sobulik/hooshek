import hooshek.athletes.athlete
import hooshek.athletes.io
import hooshek.clubs.repo
import hooshek.event.io
import hooshek.persistence.json
import hooshek.results.io
import hooshek.results.category
import hooshek.startlist.io

import collections
import csv
import datetime
import hashlib
import random
import string
import typer
import typing

app = typer.Typer()


@app.command()
def clubs():
    clubs = hooshek.clubs.repo.load()
    for club_id in sorted(clubs):
        print(clubs[club_id])


@app.command()
def athletes(
    shuffle: typing.Annotated[
        str | None,
        typer.Option(help="shuffle names to anonymize and store as file <str>"),
    ] = None,
):
    clubs = hooshek.clubs.repo.load()
    aths = hooshek.athletes.io.build(clubs)
    aths = sorted(aths, key=lambda athlete: athlete.surname)
    aths = sorted(aths, key=lambda athlete: athlete.sex)
    aths = sorted(aths, key=lambda athlete: athlete.born, reverse=True)
    if shuffle:
        for athlete in aths:
            athlete.name = (
                "".join(random.sample(athlete.name, len(athlete.name))).lower().title()
            )
            athlete.surname = (
                "".join(random.sample(athlete.surname, len(athlete.surname)))
                .lower()
                .title()
            )
        hooshek.athletes.io.dump(aths, shuffle)
    else:
        hooshek.athletes.io.dump(aths, "athletes-sorted.yaml")


@app.command()
def startlist():
    event = hooshek.event.io.load()
    clubs = hooshek.clubs.repo.load()
    aths = tuple(filter(lambda x: hasattr(x, "id"), hooshek.athletes.io.build(clubs)))

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
            if (
                athlete.sex == race.sex
                and event.eff_year - athlete.born >= race.age_min
                and event.eff_year - athlete.born <= race.age_max
            ):
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

    hooshek.startlist.io.dump(startlist, event.encoding_print)

    aths = list()
    for race in startlist["races"]:
        for athlete in race.athletes:
            aths.append(athlete)

    def comparator(a):
        if a.id.startswith(tuple(string.ascii_uppercase)):
            return a.id[0] + a.id[1:].rjust(3, "0")
        return a.id.rjust(3, "0")

    aths = sorted(aths, key=comparator)
    aths = sorted(
        aths, key=lambda athlete: athlete.club.id if athlete.club is not None else ""
    )
    club = ""
    with open("start-clubs.txt", "w", encoding=event.encoding_print) as f:
        for athlete in aths:
            curr_club = athlete.club.id if athlete.club is not None else ""
            if club != curr_club:
                f.write(
                    "\n\n--------------------------------------------------------------------\n\n"
                )
                club = curr_club
            f.write(athlete.toString())
            f.write("\n")


@app.command("import-athletes")
def import_athletes(
    file: typing.Annotated[
        typer.FileText,
        typer.Argument(
            help="csv file to import; <surname>,<name>,<f|m>,<year_of_birth>,<club>"
        ),
    ],
):
    clubs = hooshek.clubs.repo.load()

    aths = list(hooshek.athletes.io.build(clubs, False))

    reader = csv.reader(file)
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
                        raise Exception(
                            "Club "
                            + row[4]
                            + " of athlete "
                            + row[0]
                            + " not defined in clubs"
                        )
                a.id = "0"
                print("{0} already present".format(row))
                break
        if not present:
            club = None
            if len(row) > 4:
                if row[4] in clubs:
                    club = clubs[row[4]]
                else:
                    raise Exception(
                        "Club "
                        + row[4]
                        + " of athlete "
                        + row[0]
                        + " not defined in clubs"
                    )
            a = hooshek.athletes.athlete.Athlete(
                {
                    "id": "0",
                    "name": row[1],
                    "surname": row[0],
                    "born": year,
                    "sex": row[2],
                    "club": club,
                }
            )
            aths.append(a)
            print("{0} created".format(row))

    hooshek.athletes.io.dump(aths, "athletes-with-imported.yaml")


@app.command("assign-bibs")
def assign_bibs():
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
            raise Exception(
                "Athletes file athlete id " + i + " not numerated correctly"
            )
        if idCounter[i] > 1:
            raise Exception(
                "Athletes file athlete id "
                + i
                + " defined "
                + str(idCounter[i])
                + " times"
            )

    hooshek.athletes.io.dump(aths, "athletes-with-bibs.yaml")


@app.command()
def results():
    event = hooshek.event.io.load()
    clubs = hooshek.clubs.repo.load()
    start = hooshek.startlist.io.load()
    flist = hooshek.results.io.load()
    aths = tuple(filter(lambda x: hasattr(x, "id"), hooshek.athletes.io.build(clubs)))
    results = dict()
    results["name"] = event.name
    results["date"] = event.date
    results["mass"] = event.mass
    results["evals"] = list()
    for race in event.races:
        for e in hooshek.results.category.eval_categories(event.eff_year, race, True):
            hooshek.results.category.fill_category(e, event, aths, race, start, flist)
            results["evals"].append(e)

    hooshek.results.io.dump(results, event.encoding_print)


@app.command("export-slcr")
def export_slcr():
    event = hooshek.event.io.load()
    clubs = hooshek.clubs.repo.load()
    start = hooshek.startlist.io.load()
    flist = hooshek.results.io.load()
    aths = tuple(filter(lambda x: hasattr(x, "id"), hooshek.athletes.io.build(clubs)))

    slcr = []
    i = 0
    for race in event.races:
        if race.age_max < 4:
            continue
        i += 1
        r = dict()
        for e in hooshek.results.category.eval_categories(event.eff_year, race, False):
            hooshek.results.category.fill_category(e, event, aths, race, start, flist)
            r["uniqueId"] = str(i)  # string # Interní ID závodu časoměřiče
            r["resultsLayout"] = (
                "CROSS_COUNTRY_INDIVIDUAL_MASS_START"
                if event.mass
                else "CROSS_COUNTRY_INDIVIDUAL_DISTANCE"
            )  # string # layout závodu, viz. Číselník
            r["categoryYearFrom"] = (
                event.eff_year - race.age_max
            )  # int # Kategorie ročník narození od
            r["categoryYearTo"] = (
                event.eff_year - race.age_min
            )  # int # Kategorie ročník narození do
            r["gender"] = (
                race.sex.upper()
            )  # string # Pohlaví M … muži, W / L / F … ženy
            r["registeredCount"] = len(
                e["started"]
            )  # int # Počet přihlášených závodníků
            r["startedCount"] = len(
                e["started"]
            )  # int # počet odstartovaných závodníků
            r["classifiedCount"] = len(e["finished"]) - len(
                e["unfinished"]
            )  # int # Počet klasifikovaných závodníků
            r["dnsCount"] = 0  # int # Počet DNS závodníků
            r["dnfCount"] = len(e["unfinished"])  # int # Počet DNF závodníků
            r["dsqCount"] = 0  # int # Počet diskvalifikovaných závodníků
            r["dqbCount"] = 0  # int # Počet DQB závodníků
            r["npsCount"] = 0  # int # Počet NPS závodníků
            r["lapCount"] = 0  # int # Počet LAPnutých závodníků
            r["organizer"] = event.organizer  # string # Pořadatel závodu
            r["raceName"] = race.slcr_name  # string # Název závodu
            r["raceDateStart"] = (
                datetime.datetime.combine(event.date, event.start)
                if hasattr(event, "start")
                else datetime.datetime.combine(event.date, datetime.time(10))
            )  # string # Datum začátku závodu
            r["raceLocation"] = event.location  # string # Místo závodu
            r["trackLengthKm"] = (
                float(race.distance.removesuffix("m")) / 1000
            )  # float # Délka trati
            r["style"] = (
                event.style if event.style is not None else "Přespolní běh"
            )  # string # styl
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
                    a["timeMilliseconds"] = ath.time // datetime.timedelta(
                        milliseconds=1
                    )
                    if first_one is None:
                        first_one = a["timeMilliseconds"]
                    a["diffMilliseconds"] = a["timeMilliseconds"] - first_one
                r["results"].append(a)
            slcr.append(r)

    hooshek.persistence.json.dump(slcr, "slcr-export.json")


if __name__ == "__main__":
    app()
