# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:24:20 2016

@author: gray
"""

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<ChestSprite@Element>:
    facing: self.surroundings.index(False)
    graphic: 'chest-{}'.format(self.facing)

<MonsterSprite@Element>:
    graphic: 'monster-{}'.format(self.facing)

<PlayerSprite@Element>:
    graphic: 'player-{}'.format(self.facing)
""")

ChestSprite = Factory.ChestSprite
MonsterSprite = Factory.MonsterSprite
PlayerSprite = Factory.PlayerSprite
