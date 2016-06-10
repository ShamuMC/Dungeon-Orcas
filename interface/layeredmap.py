# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:18:52 2016

@author: SASedlacek
"""
import pdb
#from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (NumericProperty,ObjectProperty,ListProperty,DictProperty)
from kivy.uix.anchorlayout import AnchorLayout
from utils import SparseGridLayout,Dice
from graphics import Lights,Tiles,Sprites,BACKGROUND_TEXTURE


kv = """
<MapGrid>:
        
<LayeredMap>:
    anchor: "center"
    size_hint_x: None
    width: self.height
    _lighting: app._lighting
    canvas.before: 
        Color: 
            rgba: 1,1,1,1
        Rectangle:
            size: self.size
            pos: self.pos
            texture: self.background
    MapGrid:
        cols: root._shape
        rows: root._shape
        id: scenery
    MapGrid:
        cols: root._shape
        rows: root._shape
        id: actors
    GridLayout:
        cols: root._shape
        id: lighting
"""
Builder.load_string(kv)
class MapGrid(SparseGridLayout):
    population = ListProperty([])
    
    def populate(self,elements):
        for e in elements:
            self.add_widget(e)
            self.population.append(e)
                
                
class LayeredMap(AnchorLayout):
    _shape = NumericProperty(21)
    _map = ObjectProperty(None,force_dispatch = True)
    _level = NumericProperty(1)
    chests = ListProperty([])
    monsters = ListProperty([])
    _lighting = DictProperty({})
    background = ObjectProperty(BACKGROUND_TEXTURE)
    player = ObjectProperty(None)
    def randompos(self,low,high,condition):
        if not isinstance(low,(list,tuple)):
            low = [low,low]
        if not isinstance(high,(list,tuple)):
            high = [high,high]
        pos = [(i,j) for j in range(low[1],high[1] + 1) for i in range(low[0],high[0] + 1)]
        pos = filter(condition,pos)
        return pos[Dice(len(pos)).roll()-1]
    
    
                
    def __init__(self,**kw):
        self.background.uvsize = (self._shape,self._shape)
        super(LayeredMap, self).__init__(**kw)        
        walls = []
        actors = []
        nx,ny = self._map.shape
        for i,j in zip(*self._map.walls):
            i,j = int(i),int(j)
            
            surr = self._map.neighbors(i,j)
            if (i,j) == self._map.entrance:
                walls.append(Tiles.entrance(coords = (j,nx-i-1),surroundings = surr))
            elif (i,j) == self._map.exit:
                walls.append(Tiles.exit(coords = (j,nx-i-1),surroundings = surr))
            else: 
                walls.append(Tiles.wall(coords = (j,nx-i-1),surroundings = surr))
        self.ids.scenery.populate(walls)
        for c in self._map.chests:
            cx,cy = c.coords
            surr = self._map.neighbors(cx,cy)
            chest = Sprites.chest(coords = (cy,nx-cx-1), surroundings = surr,
                                  facing = c.facing)
            self.chests.append(chest)
            actors.append(chest)
        for m in self._map.monsters:         
            mx,my = m.coords
            surr = self._map.neighbors(mx,my)
            monster = Sprites.monster(coords = (m.mapy,nx-m.mapx-1),surroundings = surr,facing = m.facing)
            self.monsters.append(monster)
            actors.append(monster)
        p = self._map.player
        self.player = Sprites.player(coords = (p.mapy,nx-p.mapx-1),surroundings = self._map.neighbors(p.mapx,p.mapy),facing = 2)
        actors.append(self.player)
        self.ids.actors.populate(actors)
        #self.lights = {}
        for i in range(self._shape):
             for j in range(self._shape):
                 self._lighting[(i,j)] = True
                 light = Lights.lightpatch(coords = (i,j),_lighting = self._lighting)
                 self.ids.lighting.add_widget(light)
         #        self.lights[(i,j)] = light
    def update(self):
        for m,s in zip(self._map.monsters,self.monsters):
            self.update_sprite(m,s)
        self.update_sprite(self._map.player,self.player)
        self.ids.actors.do_layout()
    def update_sprite(self,actor,sprite):
        nx,ny = self._map.shape
        sprite.coords = actor.mapy,nx-actor.mapx-1
        sprite.facing = actor.facing
        sprite.surroundings = self._map.neighbors(*actor.coords)
