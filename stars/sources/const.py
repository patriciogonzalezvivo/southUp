#!/usr/bin/env python

import geojson
import os

CONST_INFO = "./constellations.json"
CONST_LINES = "./constellations.lines.json" 

const_info = geojson.load(open(CONST_INFO))
const_lines = geojson.load(open(CONST_LINES))


geometries = {}
for feature in const_lines.features:
    geometries[feature.id] = feature.geometry

for feature in const_info.features:
    feature.geometry = geometries[feature.id] 

for feature in const_info.features:
    print feature.geometry.coordinates