#!/usr/bin/env python3

import termtables

def dump_start(o, ofile):
    """dump start object to an output file"""
    header = ["  #", "         jméno         ", "ročník", "klub", "start  ", "       cíl       "]
    with open(ofile, "w", encoding="utf-8") as f:
        for race in o["races"]:
            f.write("Kategorie: {0}   Trať: {1}\n".format(race["name"], race["distance"]))
            if len(race["athletes"]) > 0:
                athletes = list()
                for a in race["athletes"]:
                    l = (a["id"], (a["name"] + " " + a["surname"])[:23], a["born"], a["club"], a["start"], "")
                    athletes.append(l)
                f.write(termtables.to_string(athletes, header=header, alignment="rlccrr"))
            f.write("\n\n")
        f.write("Powered by hooshek")

def dump_finish(o, ofile):
    """dump finish object to an output file"""
    header = [" #", " S", "         jméno         ", "ročník", "klub", "čas  ", "ztráta"]
    with open(ofile, "w", encoding="utf-8") as f:
        for race in o["races"]:
            f.write("Kategorie: {0}   Trať: {1}\n".format(race["name"], race["distance"]))
            if len(race["athletes"]) > 0:
                athletes = list()
                for a in race["athletes"]:
                    l = (a["rank"], a["rank_sokol"], (a["name"] + " " + a["surname"])[:23], a["born"], a["club"], a["time"], a["diff"])
                    athletes.append(l)
                f.write(termtables.to_string(athletes, header=header, alignment="rrlccrr"))
            f.write("\n\n")
        f.write("Powered by hooshek\n")
