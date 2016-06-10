# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:35:57 2016

@author: gray
"""

from kivy.uix.image import Image
from element import Element
from utils import DotDict
                             

from lights import LightPatch
from tiles import WallTile, ExitTile, EntranceTile
from sprites import ChestSprite, MonsterSprite, PlayerSprite

Lights = DotDict({'lightpatch': LightPatch})
Tiles = DotDict({'wall': WallTile,
                 'exit': ExitTile,
                 'entrance': EntranceTile})
Sprites = DotDict({'chest': ChestSprite,
                   'monster': MonsterSprite,
                   'player': PlayerSprite})

#BACKGROUND_TEXTURE = CoreImage('graphics/floor.png').texture
BACKGROUND_TEXTURE = Image(source = 'graphics/floor.png').texture
BACKGROUND_TEXTURE.wrap = 'repeat'