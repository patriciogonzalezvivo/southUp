#!/usr/bin/env python
import math

def y2lat(a):
  return 180.0/math.pi*(2.0*math.atan(math.exp(a*math.pi/180.0))-math.pi/2.0)

def lat2y(a):
  return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))

def distance(A, B):
    lon1 = math.radians(A[0])
    lat1 = math.radians(A[1])
    
    lon2 = math.radians(B[0])
    lat2 = math.radians(B[1])

    dlon = lon1 - lon2

    EARTH_R = 6372.8

    y = math.sqrt(
        (math.cos(lat2) * math.sin(dlon)) ** 2
        + (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)) ** 2
        )
    x = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(dlon)
    c = math.atan2(y, x)
    return EARTH_R * c