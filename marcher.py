#dependencies
from catsnake import *
from PIL import Image
from tqdm import tqdm
import math
import random

#global variables
segsize = [5,5,5]

#test function to generate a cube of random points, which takes 3 arrays defining its corners
def randomPoints(ptcount, xbounds, ybounds, zbounds):
    #list of random points
    pts = []
    #for requested amount of points
    for pt in range(ptcount):
        #choose random position
        px = scaleLinear(random.random(), 0, 1, xbounds[0], xbounds[1])
        py = scaleLinear(random.random(), 0, 1, ybounds[0], ybounds[1])
        pz = scaleLinear(random.random(), 0, 1, zbounds[0], zbounds[1])
        #add a point3 class with position to the list of points
        pts.append(point3(px, py, pz))
    #return the list of points
    return pts

#function to find the closest distance in a set of points:
def SDF(refpoint, points):
    #shortest distance = None, since 0 would result in always returning 0
    shortest = None
    #go over every point
    for p in points:
        #find distance to current point
        dist = (p - refpoint).length()
        #if no shortest distance is set or current is smaller
        if shortest == None or dist < shortest:
            shortest = dist
    return shortest

#shortest distance function for segmentized scene
def segSDF(refpoint, segs):
    #make distances array
    dists = []
    #find closest distance to points in each segment
    for s in segs:
        dists.append(SDF(refpoint, s))
    #return smallest of all dists
    return min(dists)

#function for finding out in which segment a point is
def getsegmentidx(pt):
    #divide position by segment size to get a float
    sx = pt.x()/segsize[0]
    sy = pt.y()/segsize[1]
    sz = pt.z()/segsize[2]
    #convert float to int and put in an array
    return [int(sx), int(sy), int(sz)]

#function for marching a ray through the scene
def marchray(startpt, direct, maxsteps, cutoff, maxdist, scene):
    #set current endpoint of the ray to the start position
    cpoint = startpt
    #define total distance as 0, since no steps have been taken
    totaldist = 0
    #define previous index for segmented rendering
    prev_idx = None
    #make steps
    for n in range(maxsteps):
        #calculate current index for ray
        idx = getsegmentidx(cpoint)
        #if the segment index is not equal to the previous segment index
        if prev_idx != idx:
            #clear array for relevant segments
            relsegs = []
            #relative segments to get relative to point
            relsize = [1, 0]
            #boolean for tracking if a point has been found
            foundPoint = False
            while not foundPoint:
                #make selection 1 bigger allong all axis
                relsize[0] -= 1
                relsize[1] += 1
                #loop over all segments in selection
                for iz in range(relsize[0], relsize[1]):
                    for iy in range(relsize[0], relsize[1]):
                        for ix in range(relsize[0], relsize[1]):
                            #check if not in previous selection
                            if iz == relsize[0] + 1 or iz == relsize[1] - 1:
                                if iy == relsize[0] + 1 or iy == relsize[1] - 1:
                                    if ix == relsize[0] + 1 or ix == relsize[1] - 1:
                                        #add relative position to global
                                        sx = idx[0] + ix
                                        sy = idx[1] + iy
                                        sz = idx[2] + iz
                                        try:
                                            if len(scene[sx][sy][sz]) > 0:
                                                foundPoint = True
                                                relsegs.append(scene[sx][sy][sz])
                                        except:
                                            pass
        
        #find safe step size from relative segments
        stepsize = segSDF(cpoint, relsegs)
        #make step
        cpoint = cpoint + direct.scale(stepsize)
        #add step to total distance
        totaldist += stepsize
        #set previous index to current one
        prev_idx = idx
        #if in cutoff proximity, return hit color
        if stepsize < cutoff:
            return (255, 255, 255)
        #if the ray left the scene, return background
        if totaldist > maxdist:
            return (0, 0, 0)
    #out of steps, return this color
    return (127, 127, 127)

def segmentize(points):
    scene = {}
    for p in points:
        s = getsegmentidx(p)
        try:
            scene[s[0]][s[1]][s[2]].append(p)
        except:
            try:
                scene[s[0]][s[1]] = {}
                scene[s[0]][s[1]][s[2]].append(p)
            except:
                scene[s[0]] = {}
                scene[s[0]][s[1]] = {}
                scene[s[0]][s[1]][s[2]].append(p)
    return scene


points = randomPoints(16384, [-5, 5], [-5, 5], [-5, 5])
scene = segmentize(points)

print(scene)