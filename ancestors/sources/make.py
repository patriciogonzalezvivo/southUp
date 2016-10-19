#!/usr/bin/env python
import sys, time
import requests
import json, geojson, yaml, math
from PIL import Image
import encode

max_points = 0
trip_counter = 0

#decode an encoded string
def decode(encoded, precision = 1.0 / 1e6):
    decoded = []
    previous = [0,0]
    i = 0
    #for each byte
    while i < len(encoded):
        #for each coord (lat, lon)
        ll = [0,0]
        for j in [0, 1]:
            shift = 0
            byte = 0x20
            #keep decoding bytes until you have this coord
            while byte >= 0x20:
                byte = ord(encoded[i]) - 63
                i += 1
                ll[j] |= (byte & 0x1f) << shift
                shift += 5
            #get the final value adding the previous offset and remember it for the next
            ll[j] = previous[j] + (~(ll[j] >> 1) if ll[j] & 1 else (ll[j] >> 1))
            previous[j] = ll[j]
        #scale by the precision and chop off long coords also flip the positions so
        #its the far more standard lon,lat instead of lat,lon
        decoded.append([float('%.6f' % (ll[1] * precision)), float('%.6f' % (ll[0] * precision))])
    #hand back the list of coordinates
    return decoded

def getRouteFromValhala(A, B, mode = 'auto'):
    time.sleep(1)
    KEY = 'valhalla-EzqiWWY'
    URL = 'http://valhalla.mapzen.com/route?'
    FROM_TO = '{"locations":[{"lon":'+str(A[0])+',"lat":'+str(A[1])+'},{"lon":'+str(B[0])+',"lat":'+str(B[1])+'}],"costing":"'+mode+'"}'
    RST = requests.get(URL+'json='+FROM_TO+'&api_key='+KEY)
    JSON = json.loads(RST.text)
    return decode(JSON['trip']['legs'][0]['shape'])

def getRouteFromGeoJSON(url):
    # This only works with the port-to-port JSONs of https://www.searates.com/reference/portdistance
    data = json.load(open(url))
    path = []
    for point in data[2]['path']:
        path.append([point[1], point[0]])
    return path

def parseAncester(url, people, places, features):
    yaml_file = yaml.safe_load(open(url))
    people[yaml_file['name']] = yaml_file;
    print yaml_file['name'], yaml_file['birth']['year'], "-", yaml_file['death']['year']

    global trip_counter
    global max_points

    for trip in yaml_file['legs']:
        print '- trip from', trip['from']['city'], "to", trip['to']['city']
        if not places.has_key(trip['from']['city']):
            places[trip['from']['city']] = trip['from']['coord']
        if not places.has_key(trip['to']['city']):
            places[trip['to']['city']] = trip['to']['coord']

        if trip.has_key('url'):
            line = getRouteFromGeoJSON(trip['url'])
            if len(line) > max_points:
                max_points = len(line)
            features.append(geojson.Feature(geometry=geojson.LineString(line),id=trip_counter,properties={"trip_id":trip_counter, "name": yaml_file['name'], "kind": "trip", "person_id": len(people.keys())}))
            trip_counter += 1
        else:
            line = getRouteFromValhala(trip['from']['coord'],trip['to']['coord'])
            if len(line) > max_points:
                max_points = len(line)
            features.append(geojson.Feature(geometry=geojson.LineString(line),id=trip_counter,properties={"trip_id":trip_counter, "name": yaml_file['name'], "kind": "trip", "person_id": len(people.keys())}))
            trip_counter += 1
    return 

# --------------------------------------- APP
places = {}
people = {}
features = []

# features.append(parseAncester('ppl/sofia_hamburger_firks.yaml', people, places))
# features.append(parseAncester('ppl/elias_heinrich_braun_fucks.yaml', people, places))
parseAncester('ppl/mauricio_braun_hamburger.yaml', people, places, features)
parseAncester('ppl/jose_maria_menendez_canedo.yaml', people, places, features)
parseAncester('ppl/jose_maria_menendez_canedo.yaml', people, places, features)
parseAncester('ppl/jose_fuschini_sambi.yaml', people, places, features)
parseAncester('ppl/dudley_sarsfield_brennan.yaml', people, places, features)

print max_points, trip_counter

header = 1
img = Image.new('RGBA', (max_points+header, trip_counter*2), (0,0,0,0))
pixels = img.load()

y = 0
for trip in features:
    points = trip['geometry']['coordinates']

    pixels[0,y] = encode.toRGBA(len(points))

    x = 0
    for point in points:
        pixels[x+header,y] = encode.toRGBA(point[0])
        pixels[x+header,y+1] = encode.toRGBA(point[1])
        x += 1
    y += 2
img.save(open('trips.png', 'w'))

# Add places
place_counter = 0
for place in places:
    features.append(geojson.Feature(geometry=geojson.Point(places[place]),id=place_counter,properties={"name": place, "kind": "place"}))
    place_counter += 1

feature_collection = geojson.FeatureCollection(features)
file = open('ancestors.json', 'w')
file.write(geojson.dumps(feature_collection, sort_keys=True))
file.close
