from catsnake import *
import math
import random
from PIL import Image
from tqdm import tqdm

def randomPoints(ptcount, xbounds, ybounds, zbounds):
    pts = []
    for pt in range(ptcount):
        px = scaleLinear(random.random(), 0, 1, xbounds[0], xbounds[1])
        py = scaleLinear(random.random(), 0, 1, ybounds[0], ybounds[1])
        pz = scaleLinear(random.random(), 0, 1, zbounds[0], zbounds[1])
        pts.append(point3(px, py, pz))
    return pts

def makesegs(nx, ny, nz):
    segs = []
    for x in range(nx):
        segx = []
        for y in range(ny):
            segy = []
            for z in range(nz):
                segy.append([])
            segx.append(segy)
        segs.append(segx)
    return segs

def calcsegpos(pt, lx, ly, lz, nx, ny, nz, sx, sy, sz):
    segwx = lx/nx
    segwy = ly/ny
    segwz = lz/nz
    ix = int(scaleLinear(pt.x(), sx, sx + lx, 0, nx))
    iy = int(scaleLinear(pt.y(), sy, sy + ly, 0, ny))
    iz = int(scaleLinear(pt.z(), sz, sz + lz, 0, nz))
    return [ix, iy, iz]

def segmentize(points, lx, ly, lz, nx, ny, nz, sx, sy, sz):
    segs = makesegs(nx, ny, nz)
    segwx = lx/nx
    segwy = ly/ny
    segwz = lz/nz
    for p in points:
        ix = int(scaleLinear(p.x(), sx, sx + lx, 0, nx))
        iy = int(scaleLinear(p.y(), sy, sy + ly, 0, ny))
        iz = int(scaleLinear(p.z(), sz, sz + lz, 0, nz))
        segs[ix][iy][iz].append(p)
    return segs

def SDF(refPoint, points):
    shortest = None
    for p in points:
        dist = (p - refPoint).length()
        if shortest == None or dist < shortest:
            shortest = dist
    return shortest

def marchRay(startpt, direct, maxcount, cutoff, maxdist, scene):
    cpoint = startpt
    total_dist = 0
    prev_idx = None
    for n in range(maxcount):
        idx = calcsegpos(cpoint, 10, 10, 10, sc[0], sc[1], sc[2], -5, -5, -5)
        if idx[0] > sc[0] or idx[0] < 0 or idx[1] > sc[1] or idx[1] < 0 or idx[2] > sc[2] or idx[2] < 0:
            return (0, 0, 0)
        if idx != prev_idx:
            relpts = []
            for sx in range(-1, 2):
                for sy in range(-1, 2):
                    for sz in range(-1, 2):
                        try:
                            for pt in scene[idx[0] + sx][idx[1] + sy][idx[2] + sz]:
                                relpts.append(pt)
                        except: pass
        stepsize = SDF(cpoint, relpts)
        total_dist += stepsize
        cpoint = cpoint + direct.scale(stepsize)
        prev_idx = idx
        if stepsize < cutoff:
            return (int(scaleLinear(cpoint.x(), -5, 5, 0, 255)), int(scaleLinear(cpoint.y(), -5, 5, 0, 255)), int(scaleLinear(cpoint.z(), -5, 5, 0, 255)))
        if total_dist > maxdist:
            return (0, 0, 0)
    return (0, 0, 0)

sc = [20, 20, 20]
points = randomPoints(16384, [-5, 5], [-5, 5], [-5, 5])
scene = segmentize(points, 10, 10, 10, sc[0], sc[1], sc[2], -5, -5, -5)

iw = 256
ih = 256

img = Image.new("RGB", (iw, ih), "white")
pixels = img.load()
point = point3(0, 0, -15)

for y in tqdm(range(ih)):
    for x in range(iw):
        direct = vector3(scaleLinear(x, 0, iw - 1, -1, 1), scaleLinear(y, 0, ih -1, -1, 1), 1)
        firstStep = direct.scaleZ((point.z()*-1)-5)
        startpos = point + firstStep
        if startpos.x() > 5 or startpos.x() < -5 or startpos.y() > 5 or startpos.y() < -5:
            pixels[x, y] = (0, 0, 0)
        else:
            pixels[x, y] = marchRay(startpos, direct, 32, 0.05, 25, scene)

img.save('./segtest.png')