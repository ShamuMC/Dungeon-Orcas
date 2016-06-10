# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:41:09 2016

@author: SASedlacek
"""
from kivy.properties import NumericProperty,ListProperty,ReferenceListProperty
from utils import Dice as D
from gear import numberlist as n,_gear
from kivy.event import EventDispatcher

class Chest(EventDispatcher):
    mapx = NumericProperty(0)
    mapy = NumericProperty(0)
    coords = ReferenceListProperty(mapx,mapy)
    
    inv = ListProperty([])
    level = NumericProperty(0)
    size = NumericProperty(1)
    items = ListProperty([])
    def __init__(self,**kw):
        super(Chest,self).__init__(**kw)
        self.items = n[int(self.level)]
        if len(self.items) not in [0,1]:
            d = D(len(self.items))
            for i in range(self.size):
                j = self.items[d.roll() - 1]
                self.inv.append(j)
        else:
            if len(self.items) == 1:
                self.inv.extend(self.items)
            else:
                pass
            
    def __setstate__(self,state):
        self.inv = [_gear[c][n] for c,n in state["inventory"]]
        (self.x,self.y) = state["position"]
        
    def __getstate__(self):
        return {"inventory":[(x.category,x.name) for x in self.inv],"position":(self.x,self.y)}

    
class BossChest(EventDispatcher):
    def __init__(self,level):
        self.items = n[int(level)]
        self.inv = [None]*2
        d = D(len(self.items))
        for i in [0,1]:
            self.inv[i] = self.items[d.roll()-1]