from catsnake import *
import math
import random
from PIL import Image

def SDF(refPoint, points):
    shortest = None
    for p in points:
        dist = (p - refPoint).length()
        if shortest == None or dist < shortest:
            shortest = dist
    return shortest

def randomPoints(ptcount, xbounds, ybounds, zbounds):
    pts = []
    for pt in range(ptcount):
        px = scaleLinear(random.random(), 0, 1, xbounds[0], xbounds[1])
        py = scaleLinear(random.random(), 0, 1, ybounds[0], ybounds[1])
        pz = scaleLinear(random.random(), 0, 1, zbounds[0], zbounds[1])
        pts.append(point3(px, py, pz))
    return pts

scene = randomPoints(200, [-5, 5], [-5, 5], [-5, 5])

def marchRayOrth(startPt, dir, maxcount):
    pass

v1 = vector3(12, 6, 4)
v2 = vector3(6, 3, 2)

v4 = vector3(0.5, -0.5, 0.25)

print(v1.length(), v2.length())

print(v1, v2)
v3 = v1.clamp(7)

print(v3, v3.length(), (v3*v4).clamp(v3.length()), (v3 * v4).clamp(v3.length()).length())