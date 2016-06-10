# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 10:00:33 2016

@author: SASedlacek
"""
from kivy.properties import *
from kivy.event import EventDispatcher

FACINGSTR = "wesn"

class Actor(EventDispatcher):
    mapx = NumericProperty(1)
    mapy = NumericProperty(1)
    coords = ReferenceListProperty(mapx,mapy)
    
    facing = NumericProperty(2)
    vision = NumericProperty(1)
    _alive = BooleanProperty(True)
    sprite = ObjectProperty(None)
    hp = NumericProperty(10)
    level = NumericProperty(1)
    gold = NumericProperty(0)
    stats = DictProperty(dict(zip(["Attack","Defense","Accuracy", "MaxHP",
                                   "Range","Exp+","Gold+"],[0]*7)))
    name = StringProperty("")                             
    def move(self, dx, dy):
        self.mapx += dx
        self.mapy += dy    
    
    def _loe(self):
        x,y = self.coords
        out = []
        dx,dy = {0:(0,-1),1:(0,1),2:(1,0),3:(-1,0)}[self.facing]
        for i in range(self.rang):
            x += dx
            y += dy
            out.append((x,y))
        return out
    loe = AliasProperty(_loe,None,bind = ["mapx","mapy","facing","rang"])

    def _los(self):
        x,y = self.coords
        out = []
        dx,dy = {0:(0,-1),1:(0,1),2:(1,0),3:(-1,0)}[self.facing]
        for i in range(self.vision):
            x += dx
            y += dy
            out.append((x,y))
        return out
    los = AliasProperty(_los,None,bind = ["mapx","mapy","facing","vision"])

    def _lp(self):
        x,y = self.coords
        out = []
        dx,dy = {3:(0,-1),2:(0,1),0:(1,0),1:(-1,0)}[self.facing]
        for i in range(2):
            x += dx
            y += dy
            out.append((x,y))
        return out
    lp = AliasProperty(_lp,None,bind = ["mapx","mapy","facing"])

    def _rp(self):
        x,y = self.coords
        out = []
        dx,dy = {2:(0,-1),3:(0,1),1:(1,0),0:(-1,0)}[self.facing]
        for i in range(2):
            x += dx
            y += dy
            out.append((x,y))
        return out
    rp = AliasProperty(_rp,None,bind = ["mapx","mapy","facing"])
        
    def _facestr(self):
        return FACINGSTR[self.facing]
    facestr = AliasProperty(_facestr,None,bind = ["facing"])
        
    def isat(self,x,y):
        return (x,y) == self.coords
    
    def _neighbors(self):
        return [(self.mapx,self.mapy-1),(self.mapx,self.mapy+1),
                (self.mapx+1,self.mapy),(self.mapx-1,self.mapy)]
    neighbors = AliasProperty(_neighbors,None,bind = ["mapx","mapy"])