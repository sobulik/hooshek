#!/usr/bin/env python3

import hooshek.clubs.repo

clubs = hooshek.clubs.repo.load()
for club in sorted(clubs.values(), key=lambda club: club.id):
    print(club)
