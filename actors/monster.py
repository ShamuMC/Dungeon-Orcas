# -*- coding: utf-8 -*-
"""
Created on Tue May 03 09:44:17 2016

@author: SASedlacek
"""
from actor import Actor
from kivy.properties import AliasProperty
from utils import facing,rotate,Dice


class Monster(Actor):
    """This needs a docstring"""
    def __init__(self,r = 1,kind = "melee", **kw):
        super(Monster,self).__init__(**kw)
        self.stats = {"Attack":2 ** self.level + 8,"Defense":2 ** self.level + 3,
                      "MaxHP":2 ** self.level + 8,"Accuracy":0.75,"Range":r}
        self.hp = self.maxhp
        self.kind = kind
        self.name = "Monster"
        self.vision = max(3,self.rang)
        self.playermemory = ()
    
    def __setstate__(self,state):
        self.hp = int(state["hp"])
        self.level = int(state["level"])
        self.kind = state["kind"]
        self.name = state["name"]
        self.vision = int(state["vision"])
        self.stats = state["stats"]
    def __getstate__(self):
        return {"hp":self.hp,"level":self.level,"kind":self.kind,"name":self.name,
                "vision":self.vision,"stats":self.stats}
    
    def _getstat(self,stat):
        return self.stats.get(stat,0)
    attack = AliasProperty(lambda self:self._getstat("Attack"),None,bind = ["stats"])
    defense = AliasProperty(lambda self:self._getstat("Defense"),None,bind = ["stats"])
    accuracy = AliasProperty(lambda self:self._getstat("Accuracy"),None,bind = ["stats"])
    maxhp = AliasProperty(lambda self:self._getstat("MaxHP"),None,bind = ["stats"])
    rang = AliasProperty(lambda self:self._getstat("Range"),None,bind = ["stats"])   
   
    
    def look(self,themap):
        oldfacing = self.facing
        paths = []
        directions = "2031"[self.facing/2::2]
        extra = "1032"[self.facing]
        for i in directions:
            self.facing = int(i)
            if themap.passable(*self.los[0]):
                paths.append(self.facing)
        if paths == []:
            self.facing = int(extra)
            paths.append(self.facing)
            if not themap.passable(*self.los[0],allow_player = False) or themap.player.isat(*self.los[0]):
                print "Monster.look is broken"
                
        self.facing = oldfacing
        if len(paths) <= 1:
            return int(paths[0])
        return int(paths[Dice(len(paths)).roll()-1])
        
    def move(self, themap):
        if self.facing not in range(4):  
            return
        dx,dy = facing(self,self.facing)
        nx,ny = dx + self.mapx,dy + self.mapy
        if not themap.passable(nx,ny):
            direct = self.look(themap)
            dx,dy = facing(self,direct)
        super(Monster,self).move(dx,dy)
            
            
    def ai(self, themap, engine):
        if self.hp > 0:
            lx,ly = self.lp[0]
            rx,ry = self.rp[0]
            pcoords = tuple(themap.player.coords)
            if pcoords in self.los:
                self.playermemory = pcoords
                if pcoords in self.loe:
                    engine.attack(self,themap.player)
                    
                else:
                    self.move(themap)
                    
            elif pcoords in self.lp and themap.passable(lx,ly):
                rotate(self,"snwe"[self.facing])
                
            elif pcoords in self.rp and themap.passable(rx,ry):
                rotate(self,"nswe"[self.facing])
                
            else:
                self.move(themap)
        