import hooshek.athletes.io
import hooshek.clubs.repo

import random
import typer

app = typer.Typer()


@app.command()
def clubs():
    clubs = hooshek.clubs.repo.load()
    for club_id in sorted(clubs):
        print(clubs[club_id])


@app.command()
def athletes(
    shuffle: str = typer.Option(
        None, help="shuffle names to anonymize and store as file <str>"
    ),
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


if __name__ == "__main__":
    app()
