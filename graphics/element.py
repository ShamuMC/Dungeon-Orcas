# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 09:59:45 2016

@author: SASedlacek
"""
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import (NumericProperty, BooleanProperty,
                             ReferenceListProperty, StringProperty)
                             
Builder.load_string("""
<Element>:
    source: 'atlas://graphics/tiles/'+self.graphic
""")

class Element(Image):
    graphic = StringProperty('empty')
    
    #positioning
    mapx = NumericProperty(0)
    mapy = NumericProperty(0)
    coords = ReferenceListProperty(mapx, mapy)
    
    #neighboring squares - are they occupied?
    north = BooleanProperty(False)
    west = BooleanProperty(False)
    east = BooleanProperty(False)
    south = BooleanProperty(False)
    surroundings = ReferenceListProperty(west, east, south, north)
    
    #this is only relevant for sprites
    facing = NumericProperty(0)