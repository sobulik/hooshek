#!/usr/bin/env python3

import termtables

def dump_start(o, ofile, encoding_print):
    """dump start object to an output file"""
    if o["mass"]:
        header = ["  #", "        jméno        ", "nar.", "     klub      ", "     čas     "]
    else:
        header = ["  #", "        jméno        ", "nar.", "     klub      ", " start  ", "   cíl    "]
    with open(ofile, "w", encoding=encoding_print) as f:
        isFirst = True
        for race in o["races"]:
            if isFirst:
                isFirst = False
            else:
                f.write("\n\f")
            f.write("Kategorie: {0}   Trať: {1}\n".format(race["name"], race["distance"]))
            if len(race["athletes"]) > 0:
                athletes = list()
                for a in race["athletes"]:
                    if o["mass"]:
                        l = (str(a["id"])[:3], (a["name"] + " " + a["surname"])[:21], str(a["born"])[:4], str(a["club"])[:15], "")
                    else:
                        l = (str(a["id"])[:3], (a["name"] + " " + a["surname"])[:21], str(a["born"])[:4], str(a["club"])[:15], str(a["start"])[:8], "")
                    athletes.append(l)
                if o["mass"]:
                    alignment = "rlclr"
                else:
                    alignment = "rlclrr"
                f.write(termtables.to_string(athletes, header=header, alignment=alignment))
            f.write("\nPowered by hooshek\n")

def dump_finish(o, ofile, encoding_print):
    """dump finish object to an output file"""
    header = [" #", " S", "        jméno        ", "nar.", "     klub      ", "  čas  ", "ztráta "]
    with open(ofile, "w", encoding=encoding_print) as f:
        isFirst = True
        for race in o["races"]:
            if isFirst:
                isFirst = False
            else:
                f.write("\n\f")
            f.write("Kategorie: {0} {1}  Trať: {2}\n".format(race["name"], race["desc"], race["distance"]))
            if len(race["athletes"]) > 0:
                athletes = list()
                for a in race["athletes"]:
                    l = (str(a["rank"])[:2], str(a["rank_sokol"])[:2], (a["name"] + " " + a["surname"])[:21], str(a["born"])[:4], str(a["club"])[:15], str(a["time"])[:7], str(a["diff"])[:7])
                    athletes.append(l)
                f.write(termtables.to_string(athletes, header=header, alignment="rrlclrr"))
            f.write("\nPowered by hooshek\n")
