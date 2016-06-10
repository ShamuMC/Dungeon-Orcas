# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:01:58 2016

@author: gray
"""

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty

class SparseGridLayout(FloatLayout):
    rows = NumericProperty(1)
    cols = NumericProperty(1)
    shape = ReferenceListProperty(rows, cols)
    
    def do_layout(self, *args):
        shape_hint = (1. / self.cols, 1. / self.rows)
        for child in self.children:
            child.size_hint = shape_hint
            if not hasattr(child, 'mapx'):
                child.mapx = 0
            if not hasattr(child, 'mapy'):
                child.mapy = 0
    
            child.pos_hint = {'x': shape_hint[0] * child.mapx,
                              'y': shape_hint[1] * child.mapy}
        super(SparseGridLayout, self).do_layout(*args)