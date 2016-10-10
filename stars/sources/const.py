#!/usr/bin/env python

import geojson
import os

CONST_LABELS = "./constellations.json"
CONST_LINES = "./constellations.lines.json" 
CONST_OUT = "./const.json"

const = {}
const['lines'] = geojson.load(open(CONST_LINES))
const['labels'] = geojson.load(open(CONST_LABELS))

names = {}
for feature in const['labels'].features:
    names[feature.id] = feature.properties['name']

# Fix and take geometries
id_counter = 1
for feature in const['lines'].features:
    feature['properties'] = { 'name': names[feature.id], 'id': id_counter }
    id_counter = id_counter + 1
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