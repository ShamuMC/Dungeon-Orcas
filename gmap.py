# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:58:03 2015

@author: SASedlacek
"""
from utils import Dice
from collections import defaultdict
from kivy.properties import NumericProperty,ObjectProperty,ListProperty,AliasProperty
from items import Chest
import numpy as npy
from cfg import MAPSIZE as mapsize
from lighting import LightSource as lights
from kivy.event import EventDispatcher
d7 = Dice(7)
dMap = Dice(mapsize)

#need to add "passable" method
class Map(EventDispatcher):
    """This needs a docstring"""
    monsters = ListProperty([])
    player = ObjectProperty(None)
    _level = NumericProperty(1)
    lightsources = ListProperty([])
    chests = ListProperty([])
    _Z = ObjectProperty(None)
    def __init__(self,**kw):
        super(Map,self).__init__(**kw)
        self.reset(self._level)
        
    def __setstate__(self,state):
        self.maze.seed = state["seed"]
        self.lightsources = []
        #for l in state["lightsources"]:
            #ls = LightSource()
            #ls.__setstate__(l)
            #self.lightsources.append(ls)
        self.reset(state["level"])
        self.chests = []
        for c in state["chests"]:
            ch = Chest(0)
            ch.__setstate__(c)
            self.chests.append(ch)
    def __getstate__(self):
        return {"seed":self.maze.seed,"level":self._level,
                "lightsources":[l.__getstate__() for l in self.lightsources],
                "chests":[c.__getstate__() for c in self.chests]}
    
    def neighbors(self,i,j):
        nx,ny = self._Z.shape
        return [j > 0 and self._Z[i,j-1],j < ny - 1 and self._Z[i,j+1],
                i < nx - 1 and self._Z[i+1,j],i > 0 and self._Z[i-1,j]]    
    def passable(self,i,j,allow_player = True):
        return (not self._Z[i,j] and [i,j] not in [c.coords for c in self.chests] 
                and (allow_player or [i,j] != self.player.coords))
    def reset(self,level = 1):
        self._level = level
        self._shape = self._Z.shape
        self.lightsources = []      
        self.boss = level == 5
        self.player.coords = (1,1)
        self.entrance = (0,1)
        if not self.boss:
            for monster in self.monsters:
                monster.coords = self.randompos(1,[x - 1 for x in self._shape],lambda (x,y): not self._Z[x,y])
                monster.facing = self.neighbors(*monster.coords).index(False)
                    
            self.chests = [Chest(level = self._level) for i in range(level)]
            for chest in self.chests:
                chest.coords = self.randompos(1,[x - 2 for x in self._shape],
                                               lambda (x,y): not self._Z[x,y] and
                                               sum(map(int,self.neighbors(x,y))) == 3)
                chest.facing = self.neighbors(*chest.coords).index(False)
                            
            self.exit = self.randompos([x/2-3 for x in self._shape], [x/2+4 for x in self._shape],
                                         lambda (x,y): [self._Z[x+1,y],self._Z[x,y+1],self._Z[x,y-1],self._Z[x,y]] == [False,True,True,True])
        
    def randompos(self,low,high,condition):
        if not isinstance(low,(list,tuple)):
            low = [low,low]
        if not isinstance(high,(list,tuple)):
            high = [high,high]
        pos = [(i,j) for j in range(low[1],high[1] + 1) for i in range(low[0],high[0] + 1)]
        pos = filter(condition,pos)
        return pos[Dice(len(pos)).roll()-1]
            
    @property
    def walls(self):
        return self._Z.nonzero()
    @property
    def shape(self):
        return self._Z.shape
    
    def __getitem__(self,xy):
        return self._Z[xy[0],xy[1]]
                    
    def placels(self,x,y,radius = 3,decay = None):
        self.lightsources.append(lights(self._walls,origin = (x,y),radius = radius, decay = decay))
    
    def _get_lights(self):
        lights = defaultdict(bool)
        for ls in self.lightsources:
            for xy in ls.lit:
                lights[xy] = True
        return lights
    lights = AliasProperty(_get_lights,None,bind = ["lightsources"])    