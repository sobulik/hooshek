#!/usr/bin/env python3

import clubs

clubs = clubs.load()
for club in sorted(clubs.values(), key=lambda club : club.id):
    print(club.toString())
