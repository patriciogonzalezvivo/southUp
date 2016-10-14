#!/usr/bin/env python

import geojson
import os

MW_IN = "./mw.json"
MW_OUT = "./milkway.json"

mw = geojson.load(open(MW_IN))

# Fix and take geometries
for feature in mw['features']:
    for polygon in feature['geometry']['coordinates'][0]:
        lng_prev = 0
        for coord in polygon:
            lng_diff = coord[0] - lng_prev
            if abs(lng_diff) > 180:
                lng_offset = 0
                if lng_diff > 0:
                    lng_offset = -360
                else:
                    lng_offset = 360
                coord[0] += lng_offset
            lng_prev = coord[0]

file = open(MW_OUT, 'w')
file.write(geojson.dumps(mw, sort_keys=True))
file.close()