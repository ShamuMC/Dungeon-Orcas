# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:19:59 2016

@author: gray
"""

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<WallTile@Element>:
    graphic: 'wall-{}{}{}{}'.format(*map(int,self.surroundings))

<ExitTile@Element>:
    graphic: 'exit'

<EntranceTile@Element>:
    graphic: 'entrance'
""")

WallTile = Factory.WallTile
ExitTile = Factory.ExitTile
EntranceTile = Factory.EntranceTile