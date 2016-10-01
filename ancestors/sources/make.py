#!/usr/bin/env python
import sys
import requests
import json, geojson, yaml

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

def getRouteFromValhala(A, B, mode = 'multimodal'):
    KEY = 'valhalla-EzqiWWY'
    URL = 'http://valhalla.mapzen.com/route?'
    FROM_TO = '{"locations":[{"lat":'+str(A[1])+',"lon":'+str(A[0])+'},{"lat":'+str(B[1])+',"lon":'+str(B[0])+'}],"costing":"'+mode+'"}'
    RST = requests.get(URL+'json='+FROM_TO+'&api_key='+KEY)
    JSON = json.loads(RST.text)
    print JSON
    return decode(JSON['trip']['legs'][0]['shape'])

def getRouteFromGeoJSON(url):
    # This only works with the port-to-port JSONs of https://www.searates.com/reference/portdistance
    data = json.load(open(url))
    path = []
    for point in data[2]['path']:
        path.append([point[1], point[0]])
    return path

yaml_file = yaml.safe_load(open('ppl/mauricio_braun_hamburger.yaml'))

lines = []
for trip in yaml_file['legs']:
    print 'Parsing', trip['name']
    if trip.has_key('url'):
        lines.append(getRouteFromGeoJSON(trip['url']))
    # else:
        # lines.append(getRouteFromValhala(trip['from'],trip['to']))


feature = geojson.Feature(geometry=geojson.MultiLineString(lines))
feature_collection = geojson.FeatureCollection([feature])
file = open('ancestors.json', 'w')
file.write(geojson.dumps(feature_collection, sort_keys=True))
file.close
