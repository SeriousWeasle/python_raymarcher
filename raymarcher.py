from catsnake import *
import math
import random
from PIL import Image
from tqdm import tqdm

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

scene = randomPoints(4096, [-5, 5], [-5, 5], [-5, 5])

def marchRay(startPt, direct, maxcount, cutoff):
    cpoint = startPt
    totalDist = 0
    for n in range(maxcount):
        stepSize = SDF(cpoint, scene)
        cpoint = cpoint + direct.scale(stepSize)
        totalDist += stepSize
        if stepSize < cutoff:
            return totalDist
    return 25

img = Image.new("RGB", (128, 128), "black")
pixels = img.load()
point = point3(0, 0, -7)

for y in range(128):
    for x in range(128):
        direct = vector3(scaleLinear(x, 0, 128, -1, 1), scaleLinear(y, 0, 128, -1, 1), 1)
        intensity = marchRay(point, direct, 32, 0.1)
        ir = int(scaleQuad(intensity, 0, 25, 0, 255))
        ig = int(scaleLinear(intensity, 0, 25, 0, 255))
        ib = int(scaleSqrt(intensity, 0, 25, 0, 255))
        pixels[x, y] = (ir, ig, ib)
        print("rendered pixel", x, y, " | ", ir, ig, ib)

img.save('./test.png')