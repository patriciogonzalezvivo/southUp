#!/usr/bin/env python

import geojson
import os

CONST_LABELS = "./constellations.json"
CONST_LINES = "./constellations.lines.json" 
CONST_OUT = "./const.json"

const = {}
const['lines'] = geojson.load(open(CONST_LINES))
const['labels'] = geojson.load(open(CONST_LABELS))

# Fix and take geometries
for feature in const['lines'].features:
    for line in feature.geometry.coordinates:
        lng_prev = 0
        for coord in line:
            lng_diff = coord[0] - lng_prev
            if abs(lng_diff) > 180:
                lng_offset = 0
                if lng_diff > 0:
                    lng_offset = -360
                else:
                    lng_offset = 360
                coord[0] += lng_offset
            lng_prev = coord[0]




file = open(CONST_OUT, 'w')
file.write(geojson.dumps(const, sort_keys=True))
file.close()