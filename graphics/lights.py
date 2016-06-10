# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:26:05 2016

@author: gray
"""

from element import Element
from kivy.lang import Builder
from kivy.properties import DictProperty,AliasProperty

Builder.load_string("""
<LightPatch>:
    graphic: 'empty' if self.lit else 'dark'
""")

#This is in a separate file so that you can add a torch graphic if you want,
#or any other kind of light source I guess!

class LightPatch(Element):
    _lighting = DictProperty({})
    def _lit(self):
        if not self._lighting:
            return True
        return self._lighting[(self.mapx,self.mapy)]
    lit = AliasProperty(_lit,None,bind = ["_lighting"])
