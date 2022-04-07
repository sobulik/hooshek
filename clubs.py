#!/usr/bin/env python3

import clubs.io

clubs = clubs.io.load()
for club in sorted(clubs.values(), key=lambda club : club.id):
    print(club.toString())
