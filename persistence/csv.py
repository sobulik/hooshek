
import csv
import io

def dump_finish(o, ofile, encoding_print):

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Category', 'Description', 'Sex', 'Distance',
                    'Rank', 'Sokol Rank', 'Name', 'Surname', 'Club', 'Birth Year',
                    'Start Time', 'Finish Time', 'Total Time', 'Diff'])

    # Write data
    for race in o["races"]:
        for athlete in race["athletes"]:
            row = [
                race["name"],
                race["desc"],
                race["sex"],
                race["distance"],
                athlete["rank"],
                athlete["rank_sokol"],
                athlete["name"],
                athlete["surname"],
                athlete["club"],
                athlete["born"],
                athlete["start"],
                athlete["finish"],
                athlete["time"],
                athlete["diff"]
            ]
            writer.writerow(row)

    with open(ofile, 'w', encoding=encoding_print) as f:
        f.write(output.getvalue())
