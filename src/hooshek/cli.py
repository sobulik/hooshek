import hooshek.athletes.athlete
import hooshek.athletes.io
import hooshek.clubs.repo
import hooshek.event.io
import hooshek.startlist.io

import csv
import datetime
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


@app.command("assing-bibs")
def assign_bibs():
    pass


if __name__ == "__main__":
    app()
