# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:26:14 2016

@author: SASedlacek
"""

def facing(actor,direction):
    dx,dy = [(0,-1),(0,1),(1,0),(-1,0)][direction]
    newface = {(0,-1):0,(0,1):1,(1,0):2,(-1,0):3}[(dx,dy)]
    if actor.facing != newface:
        actor.facing = newface
        return (0,0)
    return (dx,dy)
    
def rotate(actor, direction):
    newface = {"n":3,"e":1,"s":2,"w":0}[direction]
    actor.facing = newface
    return